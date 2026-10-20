"""Local, synthetic human review queue with version-bound decisions and rollback.

Single-writer classroom store. No network effects or arbitrary command execution.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timezone


def fingerprint(body, sources, release):
    return hashlib.sha256(json.dumps(
        {"body": body, "sources": sources, "release": release},
        sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def save(folder, data):
    path = Path(folder)
    with tempfile.NamedTemporaryFile("w", dir=path, prefix=".state-", delete=False) as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
        temporary = handle.name
    os.replace(temporary, path / "queue.json")


def read(folder):
    data = json.loads((Path(folder) / "queue.json").read_text())
    if data.get("schema") != 1 or not isinstance(data.get("history"), list):
        raise ValueError("invalid queue state")
    item = data["item"]
    if item["revision"] != fingerprint(item["body"], item["sources"], item["release"]):
        raise ValueError("artifact integrity mismatch")
    return data


def event(data, kind, **fields):
    data["history"].append({"sequence": len(data["history"]) + 1,
                            "at": datetime.now(timezone.utc).isoformat(),
                            "kind": kind, **fields})


def init(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=False)
    body = "Please provide the browser version and a clean-session reproduction."
    sources = [{"id": "KB-REVIEW-1", "text": "Collect browser version and clean-session reproduction. Cause remains unverified."}]
    item = {"id": "DRAFT-1", "body": body, "sources": sources, "release": "v1",
            "revision": fingerprint(body, sources, "v1"), "status": "pending", "decision": None}
    data = {"schema": 1, "active_release": "v1", "releases": {
        "v1": {"knowledge": "v1", "validator": "v1"}},
        "item": item, "effects": [], "history": []}
    event(data, "created", revision=item["revision"])
    save(folder, data)
    return data


def revise(folder, body):
    if not isinstance(body, str) or not body.strip() or len(body) > 4000:
        raise ValueError("body must contain 1–4000 characters")
    data = read(folder)
    item = data["item"]
    if item["status"] == "applied":
        raise ValueError("applied artifact is immutable; start a separate exercise")
    previous = dict(item)
    item.update(body=body, release=data["active_release"], decision=None, status="pending")
    item["revision"] = fingerprint(body, item["sources"], item["release"])
    event(data, "revised", previous=previous, revision=item["revision"])
    save(folder, data)
    return data


def review(folder, revision, verdict, reviewer, comment=""):
    if verdict not in {"approved", "rejected", "changes_requested"}:
        raise ValueError("invalid verdict")
    if not reviewer.strip() or len(reviewer) > 100 or len(comment) > 4000:
        raise ValueError("reviewer and bounded comment required")
    data = read(folder)
    item = data["item"]
    if revision != item["revision"] or item["release"] != data["active_release"]:
        raise ValueError("stale review")
    if item["status"] == "applied":
        raise ValueError("applied artifact is immutable")
    item["status"] = verdict
    item["decision"] = {"revision": revision, "verdict": verdict, "reviewer": reviewer, "comment": comment}
    event(data, "reviewed", **item["decision"])
    save(folder, data)
    return data


def apply(folder, revision):
    data = read(folder)
    item = data["item"]
    if revision != item["revision"] or item["release"] != data["active_release"]:
        raise ValueError("stale approval")
    if item["status"] == "applied":
        return data  # Exactly the same synthetic effect is already recorded.
    decision = item["decision"]
    if item["status"] != "approved" or not decision or decision["revision"] != revision:
        raise ValueError("matching approval required")
    # Effect and state transition share one atomic local document.
    data["effects"].append({"kind": "local_review_status", "item_id": item["id"], "revision": revision})
    item["status"] = "applied"
    event(data, "applied", revision=revision)
    save(folder, data)
    return data


def release(folder, name, knowledge, validator):
    if not all(isinstance(x, str) and x and len(x) <= 50 for x in [name, knowledge, validator]):
        raise ValueError("invalid release name")
    if knowledge != validator:
        raise ValueError("knowledge/validator version mismatch")
    data = read(folder)
    manifest = {"knowledge": knowledge, "validator": validator}
    if name in data["releases"] and data["releases"][name] != manifest:
        raise ValueError("immutable release identity conflict")
    data["releases"][name] = manifest
    old = data["active_release"]
    data["active_release"] = name
    if old != name and data["item"]["status"] != "applied":
        data["item"]["decision"] = None
        data["item"]["status"] = "pending"
    # Keep pending work, but require revalidation/revision under this release.
    event(data, "release_activated", previous=old, current=name)
    save(folder, data)
    return data


def rollback(folder, name):
    data = read(folder)
    if name not in data["releases"]:
        raise ValueError("unknown rollback version")
    old = data["active_release"]
    data["active_release"] = name
    event(data, "rollback", previous=old, current=name)
    # Approval cannot silently revive after crossing a release boundary.
    if data["item"]["status"] != "applied":
        data["item"]["decision"] = None
        data["item"]["status"] = "pending"
    save(folder, data)
    return data


def rehearse(folder):
    init(folder)
    original = read(folder)["item"]["revision"]
    review(folder, original, "approved", "synthetic-reviewer", "Classroom rehearsal; no human review claimed.")
    revise(folder, "Please share your browser version and reproduction steps; the cause is unverified.")
    checks = {}
    try:
        apply(folder, original)
        checks["stale_approval_rejected"] = False
    except ValueError:
        checks["stale_approval_rejected"] = True
    before = read(folder)
    try:
        release(folder, "bad", "v2", "v1")
        checks["mismatched_release_rejected"] = False
    except ValueError:
        checks["mismatched_release_rejected"] = read(folder) == before
    release(folder, "v2", "v2", "v2")
    rollback(folder, "v1")
    checks["pending_work_preserved"] = read(folder)["item"]["body"] == before["item"]["body"]
    current = read(folder)["item"]["revision"]
    review(folder, current, "approved", "synthetic-reviewer")
    apply(folder, current)
    apply(folder, current)
    checks["one_local_effect"] = len(read(folder)["effects"]) == 1
    report = {"mode": "automated rehearsal; not human approval evidence", "checks": checks,
              "passed": all(checks.values())}
    (Path(folder) / "report.json").write_text(json.dumps(report, indent=2))
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["init", "show", "revise", "review", "apply", "release", "rollback", "rehearse"])
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--body")
    p.add_argument("--revision")
    p.add_argument("--verdict", choices=["approved", "rejected", "changes_requested"])
    p.add_argument("--reviewer", default="learner")
    p.add_argument("--comment", default="")
    p.add_argument("--version")
    p.add_argument("--knowledge")
    p.add_argument("--validator")
    args = p.parse_args(argv)
    needed = {"revise": ["body"], "review": ["revision", "verdict"], "apply": ["revision"],
              "release": ["version", "knowledge", "validator"], "rollback": ["version"]}
    for field in needed.get(args.action, []):
        if getattr(args, field) is None:
            p.error("--" + field + " is required")
    actions = {
        "init": lambda: init(args.out), "show": lambda: read(args.out),
        "revise": lambda: revise(args.out, args.body),
        "review": lambda: review(args.out, args.revision, args.verdict, args.reviewer, args.comment),
        "apply": lambda: apply(args.out, args.revision),
        "release": lambda: release(args.out, args.version, args.knowledge, args.validator),
        "rollback": lambda: rollback(args.out, args.version),
        "rehearse": lambda: rehearse(args.out),
    }
    result = actions[args.action]()
    print(json.dumps(result, indent=2))
    return 1 if args.action == "rehearse" and not result["passed"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError) as error:
        print("Queue stopped: " + str(error), file=sys.stderr)
        sys.exit(2)
