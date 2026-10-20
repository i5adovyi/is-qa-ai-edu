"""Single-process durable fixture store and append-only event stream."""

from datetime import datetime, timezone
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import os
import tempfile

from .contracts import HarnessError


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class Store:
    def __init__(self, path, ticket=None, run_id=None):
        self.path = Path(path)
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise HarnessError("store_corrupt", "The durable store could not be loaded.") from exc
        elif ticket is not None:
            self.data = {
                "version": 1,
                "run_id": run_id,
                "ticket": ticket,
                "drafts": [],
                "tags": [],
                "idempotency": {},
                "writes": 0,
            }
            self.persist()
        else:
            raise HarnessError("missing_store", "The run's durable store is missing.")
        if type(self.data) is not dict:
            raise HarnessError("store_corrupt", "Store must be a JSON object.")
        if self.data.get("version") != 1:
            raise HarnessError("store_version", "Unsupported store version.")
        if (
            type(self.data.get("ticket")) is not dict
            or type(self.data.get("drafts")) is not list
            or type(self.data.get("tags")) is not list
            or type(self.data.get("idempotency")) is not dict
            or type(self.data.get("writes")) is not int
            or self.data["writes"] < 0
            or self.data["writes"] != len(self.data["idempotency"])
        ):
            raise HarnessError("store_corrupt", "Store structure or operation counts are invalid.")
        if run_id is not None and self.data.get("run_id") != run_id:
            raise HarnessError("store_scope", "Store belongs to a different run.")

    def persist(self):
        atomic_json(self.path, self.data)

    def mutate(self, tool, arguments, key):
        if not key or not isinstance(key, str) or len(key) > 160:
            raise HarnessError("idempotency_required", "Mutation requires an idempotency key.")
        fingerprint = digest({"tool": tool, "arguments": arguments})
        previous = self.data["idempotency"].get(key)
        if previous is not None:
            if previous["fingerprint"] != fingerprint:
                raise HarnessError("idempotency_conflict", "Key was used for a different request.")
            return {**previous["result"], "replayed": True}
        # Do not expose an uncommitted effect or replay record in memory if I/O fails.
        next_data = deepcopy(self.data)
        if tool == "save_draft":
            record = {
                "draft_id": f"D-{len(next_data['drafts']) + 1:03}",
                **arguments,
            }
            next_data["drafts"].append(record)
            result = {"draft_id": record["draft_id"], "saved": True}
        elif tool == "add_tag":
            if arguments["tag"] not in next_data["tags"]:
                next_data["tags"].append(arguments["tag"])
            result = {"tag": arguments["tag"], "saved": True}
        else:
            raise HarnessError("invalid_mutation", "Unsupported store mutation.")
        next_data["writes"] += 1
        next_data["idempotency"][key] = {"fingerprint": fingerprint, "result": result}
        # Effect and deduplication record live in the same atomic JSON replacement.
        atomic_json(self.path, next_data)
        self.data = next_data
        return {**result, "replayed": False}


class Trace:
    def __init__(self, path, run_id):
        self.path = Path(path)
        self.run_id = run_id
        self.path.parent.mkdir(parents=True, exist_ok=True)
        events = read_trace(self.path) if self.path.exists() else []
        if events and events[0]["run_id"] != run_id:
            raise HarnessError("trace_scope", "Trace belongs to a different run.")
        self.sequence = len(events)

    def emit(self, event, **fields):
        self.sequence += 1
        record = {
            "sequence": self.sequence,
            "at": datetime.now(timezone.utc).isoformat(),
            "run_id": self.run_id,
            "event": event,
            **fields,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical(record) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return record


def read_trace(path):
    events = []
    with Path(path).open(encoding="utf-8") as handle:
        for index, line in enumerate(handle, 1):
            if not line.strip():
                raise HarnessError("invalid_trace", f"Empty trace record at line {index}.")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise HarnessError("invalid_trace", f"Malformed trace line {index}.") from exc
            if (type(record) is not dict or type(record.get("sequence")) is not int
                    or record["sequence"] != index
                    or type(record.get("run_id")) is not str
                    or type(record.get("event")) is not str):
                raise HarnessError("invalid_trace", f"Invalid sequence at line {index}.")
            if events and record.get("run_id") != events[0].get("run_id"):
                raise HarnessError("invalid_trace", "Mixed run IDs.")
            events.append(record)
    return events
