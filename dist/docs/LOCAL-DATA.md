# Keep your learning records between sessions

The local launcher stores portal learning state in a **SQLite database on your computer**. The hosted OpenAI Site continues to store state in the browser. Neither mode automatically uploads personal progress to GitHub or synchronizes it with the other mode.

| Where you learn | Durable records | What connects another session |
| --- | --- | --- |
| `python3 academy.py local` | `.academy-data/progress.sqlite3` in this project, unless `--data-dir` selects another location | The same project/data directory |
| Hosted OpenAI Site | That Site origin's browser storage | The same browser profile and Site URL |
| A new clone or prepared new-account folder | A new, empty local database | Import a progress JSON or restore your database backup |

The database contains portal progress: attempts, drafts, notes, tutor feedback you saved, incident attempts, reveal choices, recall history, and preferences. It does **not** automatically capture Codex conversations, files written by lab commands, or material in another browser's hosted storage. Keep lab evidence under `work/` and back it up separately.

## Start and resume

```sh
python3 academy.py local
```

Leave the server terminal open while using the portal. Stop with Ctrl+C. Start the same command next time. The data directory is relative to the project, not the terminal's working directory. Changing the OpenAI account, browser, or local port does not change that project's database.

The portal reports the storage mode and save status. Wait for confirmation that your latest change is saved before closing a tab or stopping the server. If a save fails, export your current progress and resolve the error before continuing elsewhere. Local browser storage remains a recovery aid; it is not proof that the database write succeeded.

Multiple tabs use revision checks. An older tab must not silently overwrite records saved by a newer tab. If a conflict is reported, the portal pauses for a choice: **Merge my work into the database** or **Use database copy**. Download both versions before choosing if either contains work you need. The merge keeps the database's current drafts and preserves conflicting browser drafts and history rather than silently replacing them. Avoid working in several tabs at once when you do not need to.

## Import earlier browser progress

In the original browser or hosted Site, choose **Export my progress**. In the local portal choose **Import progress**, then check an attempt, a note, and the save status. Do this before clearing the original browser storage.

When existing browser work differs from the database, including an empty database, the portal asks whether to merge that work or use the database copy. It offers downloads of both versions. Choose deliberately; records from every browser do not combine automatically. Recovery copies are also available from Progress. If the server becomes unavailable, editing can continue with an unsaved warning; export that work, restart the server, and retry the connection to reconcile it.

Exported JSON is readable personal learning data. Keep it private and outside source directories. It is the supported way to transfer records between local and hosted portals.

## Separate learners, courses, or data locations

```sh
python3 academy.py local --data-dir ../my-academy-data
```

This selects a different database directory. Use the same argument on later starts. The command's relative path is resolved from your current terminal directory; use an absolute path if you want to avoid ambiguity.

Use separate data directories for different learners. A directory on your computer is not an authenticated multi-user service. The launcher binds only to `127.0.0.1`; do not expose it through a tunnel or change it into a public server. Operating-system permissions protect the SQLite file; it is not encrypted by the academy. Keep the directory out of shared folders if it contains private records.

## Inspect and back up

After the first local launch has created the database:

```sh
python3 academy.py status
python3 academy.py backup --output ../academy-progress-backup.sqlite3
```

`status` reports the database path, identity, revision, and whether state is present. It does not print the contents of your attempts. `backup` uses SQLite's backup mechanism, so it can run while the portal is serving. The destination file must not exist; use a new name for each backup.

For a selected data directory, include it on both commands:

```sh
python3 academy.py status --data-dir ../my-academy-data
python3 academy.py backup --data-dir ../my-academy-data --output ../my-progress-backup.sqlite3
```

Do not copy just a live `progress.sqlite3` file manually: SQLite may also have active journal files. Use the backup command. Back up before moving the project, replacing a local copy, or experimenting with the application. Keep more than one dated backup and test restoration before relying on a backup for a computer migration.

## Restore without overwriting your current work

1. Stop local academy servers using the destination profile.
2. Keep the original data directory unchanged.
3. Create a **new empty directory** for recovery.
4. Copy your SQLite backup into that directory and name the copy `progress.sqlite3`.
5. Start the academy with `--data-dir` pointing to the recovery directory.
6. Check the save status, an attempt, a note, and a fresh small update. Keep the previous directory and backup until you have verified the restored copy.

You can use your file manager for steps 3–4. The following cross-platform Python command creates a new recovery directory and refuses an existing one:

```sh
python3 -c "from pathlib import Path; import shutil; p=Path('../academy-restored-data'); p.mkdir(); shutil.copy2('../academy-progress-backup.sqlite3', p/'progress.sqlite3')"
python3 academy.py local --data-dir ../academy-restored-data
```

A corrupt or unavailable database produces an error rather than silently replacing it with an empty one. Preserve the file and recover to a separate directory from a known backup or import a saved progress JSON into a new profile.

## What GitHub and downloads contain

`.academy-data/`, SQLite files, runtime records, and normal progress exports are excluded from Git and course packaging. They are **not** a backup just because your course source was pushed. Arbitrary file names or deliberate `git add -f` can bypass protections: never put personal transcripts or secrets into course source folders.

Source/portable ZIPs and newly prepared Sites contain the course, not your learner database. The new-account preparation process resets the Site identity and leaves your current data where it was. See [NEW-ACCOUNT.md](NEW-ACCOUNT.md).
