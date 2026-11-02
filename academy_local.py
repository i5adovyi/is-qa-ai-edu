"""Durable local progress storage. Stdlib only; private data never belongs in dist/."""
import json
import os
from contextlib import contextmanager
from pathlib import Path
import secrets
import sqlite3
import stat
import uuid

MAX_BODY = 8 * 1024 * 1024
SCHEMA_VERSION = 1


def is_link(path):
    """Windows directory junctions can redirect access just like symlinks."""
    try:
        info = path.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return False
    return stat.S_ISLNK(info.st_mode) or (
        os.name == "nt" and info.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT
    )


def has_symlink(path, boundary):
    current = Path(path)
    boundary = Path(boundary)
    while current != boundary:
        if is_link(current) or current.parent == current:
            return True
        current = current.parent
    return is_link(boundary)


def unlinked_files(path, boundary):
    """Prune links before descent, including a junction back to an ancestor."""
    if has_symlink(path, boundary):
        return
    if path.is_file():
        yield path
    elif path.is_dir():
        for parent, dirs, files in os.walk(path):
            parent = Path(parent)
            dirs[:] = [name for name in dirs if not is_link(parent / name)]
            for name in files:
                item = parent / name
                if not is_link(item) and item.is_file():
                    yield item


class StateError(ValueError):
    pass


class ConflictError(StateError):
    def __init__(self, revision):
        self.revision = revision
        super().__init__("Progress changed in another tab. Reload or export your draft before merging.")


def validate_state(state):
    """Check the portable progress envelope, without deleting unknown edition fields."""
    if not isinstance(state, dict) or type(state.get("version")) is not int or state["version"] not in (1, 2):
        raise StateError("Unsupported progress record: expected version 1 or 2.")
    for key in ("done", "bookmarks", "gates"):
        if not isinstance(state.get(key), list):
            raise StateError("Invalid progress record: {} must be an array.".format(key))
    for key in ("notes", "quiz"):
        if not isinstance(state.get(key), dict):
            raise StateError("Invalid progress record: {} must be an object.".format(key))
    if state["version"] == 2:
        if not isinstance(state.get("exercises"), dict):
            raise StateError("Invalid progress record: exercises must be an object.")
        for key in ("retention", "onboarding", "intervals"):
            if not isinstance(state.get(key), list):
                raise StateError("Invalid progress record: {} must be an array.".format(key))
    try:
        encoded = json.dumps(state, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    except (ValueError, TypeError, RecursionError) as exc:
        raise StateError("Progress must contain finite JSON values: {}".format(exc))
    if len(encoded.encode("utf-8")) > MAX_BODY:
        raise StateError("Progress exceeds the 8 MiB limit. Export a backup and shorten large notes.")
    return encoded


def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise StateError("Duplicate JSON field: {}".format(key))
            result[key] = value
        return result

    def constant(_):
        raise StateError("JSON must not contain NaN or Infinity.")

    return json.loads(data, object_pairs_hook=pairs, parse_constant=constant)


class ProgressDatabase:
    def __init__(self, path, create=True):
        self.path = Path(path).expanduser().resolve()
        self.csrf_token = secrets.token_urlsafe(32)
        if not create and not self.path.is_file():
            raise StateError("No local database at {}. Start the local academy first.".format(self.path))
        if create:
            self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        is_new = not self.path.exists()
        if is_new:
            # Restrict permissions before SQLite writes learner data.
            descriptor = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(descriptor)
        try:
            with self.connection() as db:
                db.execute("BEGIN IMMEDIATE")
                if is_new:
                    db.execute("CREATE TABLE progress (singleton INTEGER PRIMARY KEY CHECK(singleton=1), "
                               "database_id TEXT NOT NULL, revision INTEGER NOT NULL CHECK(revision>=0), state TEXT)")
                    db.execute("INSERT INTO progress VALUES (1, ?, 0, NULL)", (str(uuid.uuid4()),))
                    db.execute("PRAGMA user_version = {}".format(SCHEMA_VERSION))
                elif db.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
                    raise StateError("Unsupported local database schema. Keep the file and restore a known backup.")
                if db.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                    raise StateError("Local database integrity check failed. Keep the file and restore a backup.")
                self._read(db)
            # WAL allows reads while another browser tab commits; FULL preserves committed writes.
            with self.connection() as db:
                db.execute("PRAGMA journal_mode = WAL")
        except (sqlite3.Error, OSError, ValueError) as exc:
            raise StateError("Cannot open local database {}: {}. The existing file was not reset.".format(self.path, exc))

    @contextmanager
    def connection(self):
        db = sqlite3.connect(str(self.path), timeout=5)
        try:
            db.execute("PRAGMA synchronous = FULL")
            with db:
                yield db
        finally:
            db.close()

    def _read(self, db):
        row = db.execute("SELECT database_id, revision, state FROM progress WHERE singleton=1").fetchone()
        if not row or not isinstance(row[0], str) or not row[0] or type(row[1]) is not int or row[1] < 0:
            raise StateError("Local database metadata is invalid.")
        if db.execute("SELECT count(*) FROM progress").fetchone()[0] != 1:
            raise StateError("Local database contains an unexpected number of progress records.")
        state = strict_json(row[2]) if row[2] is not None else None
        if state is not None:
            validate_state(state)
        return {"databaseId": row[0], "revision": row[1], "state": state}

    def read(self):
        with self.connection() as db:
            return self._read(db)

    def write(self, revision, state):
        if type(revision) is not int or revision < 0:
            raise StateError("revision must be a nonnegative integer.")
        encoded = validate_state(state)
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            current = self._read(db)
            if current["revision"] != revision:
                raise ConflictError(current["revision"])
            next_revision = revision + 1
            db.execute("UPDATE progress SET revision=?, state=? WHERE singleton=1 AND revision=?",
                       (next_revision, encoded, revision))
        return next_revision

    def backup(self, output):
        output = Path(output).expanduser().resolve()
        if not output.parent.is_dir():
            raise StateError("Backup output directory does not exist: {}".format(output.parent))
        try:
            descriptor = os.open(str(output), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise StateError("Backup output already exists; choose a new filename: {}".format(output))
        os.close(descriptor)
        try:
            with self.connection() as source:
                destination = sqlite3.connect(str(output))
                try:
                    source.backup(destination)
                    if destination.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                        raise StateError("Backup integrity check failed.")
                finally:
                    destination.close()
        except Exception:
            output.unlink()
            raise
        return output
