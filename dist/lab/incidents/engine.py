"""Workspace creation, bounded execution, and evidence-preserving checks."""
import copy
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from .scenarios import CONTRACTS, IDS, STARTERS, TITLES, boundary_scenarios, evidence, scenario

VERSION = 1
MAX_OUTPUT = 65536
RUNNER = """import json, runpy, sys
worker = runpy.run_path(sys.argv[1])
result = worker["handle"](json.load(sys.stdin))
print(json.dumps(result, allow_nan=False))
"""


def _json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def _hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _record(root, kind, result):
    """Retain every execution; convenience 'latest' files are never the only copy."""
    result = dict(result)
    result["at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for name, field in (("student.py", "worker_sha256"), ("input.json", "input_sha256")):
        if field not in result:
            path = contained(root, name)
            result[field] = _hash(path) if path.is_file() else None
    for number in range(1, 100001):
        relative = "runs/%s-%05d.json" % (kind, number)
        target = contained(root, relative)
        try:
            with target.open("x", encoding="utf-8") as stream:
                result["record"] = relative
                stream.write(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
            break
        except FileExistsError:
            continue
    else:
        raise ValueError("Run history is full; preserve this workspace and start another.")
    _json(contained(root, "runs/latest.json" if kind == "run" else "runs/check.json"), result)
    return result


def contained(root, relative):
    relative = Path(relative)
    if relative.is_absolute():
        raise ValueError("Use a path relative to the incident workspace.")
    candidate = (root / relative).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("Path must stay inside the incident workspace.")
    return candidate


def load_workspace(path):
    root = Path(path).resolve()
    manifest_path = contained(root, ".incident.json")
    if not manifest_path.is_file():
        raise ValueError("Not an initialized incident workspace.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION or manifest.get("incident") not in IDS:
        raise ValueError("Unsupported incident workspace version or ID.")
    return root, manifest


def _git_fixture(root):
    repo = root / "repository"
    (repo / "tests").mkdir(parents=True)
    (repo / "tools").mkdir()
    (repo / "empty_tests").mkdir()
    (repo / "app.py").write_text(
        "def remaining_budget(limit, used):\n"
        "    return max(0, limit - used)\n", encoding="utf-8")
    (repo / "tests" / "test_app.py").write_text(
        "import unittest\nfrom app import remaining_budget\n\n"
        "class BudgetTests(unittest.TestCase):\n"
        "    def test_remaining(self): self.assertEqual(remaining_budget(10, 3), 7)\n"
        "    def test_boundary(self): self.assertEqual(remaining_budget(10, 10), 0)\n"
        "    def test_over(self): self.assertEqual(remaining_budget(10, 11), 0)\n", encoding="utf-8")
    (repo / "tools" / "check.py").write_text(
        "import json\nfrom pathlib import Path\nimport unittest\n\n"
        "root = Path(__file__).resolve().parents[1]\n"
        "suite = unittest.defaultTestLoader.discover(str(root / 'empty_tests'))\n"
        "result = unittest.TextTestRunner().run(suite)\n"
        "print(json.dumps({'discovered': suite.countTestCases(), 'failures': len(result.failures)}))\n",
        encoding="utf-8")
    (repo / "operator-notes.txt").write_text("Release notes awaiting review.\n", encoding="utf-8")
    (repo / "SETUP.md").write_text(
        "Legacy setup: run tools/check.py; a zero exit code means the project is ready.\n"
        "This inherited document has not been audited.\n", encoding="utf-8")
    (repo / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
    commands = [
        ["git", "init", "-q"],
        ["git", "add", "."],
        ["git", "-c", "user.name=Incident fixture", "-c", "user.email=fixture@example.invalid",
         "-c", "commit.gpgsign=false", "commit", "-qm", "Seed fictional inherited project"],
    ]
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    for command in commands:
        subprocess.run(command, cwd=str(repo), env=env, capture_output=True, check=True, timeout=15)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(repo), env=env, text=True).strip()
    (repo / "operator-notes.txt").write_text(
        "Release notes awaiting review.\nHuman draft: retain this investigation note and my wording.\n",
        encoding="utf-8")
    return revision


def initialize(case, path, variant="primary", project="support"):
    if case not in IDS or variant not in {"primary", "transfer"}:
        raise ValueError("Unknown incident or variant.")
    if project not in {"support", "qa", "research"}:
        raise ValueError("Choose support, qa, or research.")
    requested = Path(path).expanduser()
    if requested.exists() or requested.is_symlink():
        raise ValueError("Workspace already exists; choose a new path. Nothing was overwritten.")
    root = requested.resolve()
    root.mkdir(parents=True)
    (root / "evidence").mkdir()
    (root / "runs").mkdir()
    data = scenario(case, variant)
    protected = []
    if case == "INC-01":
        revision = _git_fixture(root)
        data["current_revision"] = revision
        for row in data["reports"] + data["executions"]:
            if row["revision"] == "current":
                row["revision"] = revision
        protected.extend(["repository/app.py", "repository/tests/test_app.py", "repository/operator-notes.txt"])
    if case == "INC-CAPSTONE":
        data["project"] = project
    _json(root / "input.json", data)
    (root / "student.py").write_text(STARTERS[case], encoding="utf-8")
    (root / "CONTRACT.md").write_text("# Behavioral contract\n\n" + CONTRACTS[case] + "\n", encoding="utf-8")
    (root / "brief.md").write_text(
        "# " + case + " — " + TITLES[case] + "\n\n"
        "Read the handover and input, then record competing hypotheses before changing code.\n"
        "Implement `handle(data)` in student.py according to CONTRACT.md. Keep evidence unchanged.\n"
        "Use run for the current input; check also exercises transfer and boundary workloads.\n"
        "A green checker establishes only its listed executable assertions. Your explanation,\n"
        "evidence provenance, stakeholder questions, and recovery plan still need human review.\n"
        "This is a deterministic local simulator, not a real service, security boundary,\n"
        "distributed transaction engine, or production load test. Student Python runs with your permissions.\n"
        "Guidance is closed until you save an attempt; opening reference.py yourself reveals spoilers.\n",
        encoding="utf-8")
    for name, text in evidence(case).items():
        (root / "evidence" / name).write_text(text, encoding="utf-8")
        protected.append("evidence/" + name)
    protected.extend(["input.json", "CONTRACT.md"])
    _json(root / ".incident.json", {
        "version": VERSION, "incident": case, "variant": variant, "project": project,
        "baseline": {name: _hash(root / name) for name in protected},
    })
    return root


def preserved(root, manifest):
    changed = []
    for name, digest in manifest["baseline"].items():
        path = contained(root, name)
        if not path.is_file() or _hash(path) != digest:
            changed.append(name)
    return changed


def invoke(root, data, timeout=5):
    student = contained(root, "student.py")
    if not student.is_file():
        raise ValueError("student.py is missing.")
    try:
        proc = subprocess.run([sys.executable, "-I", "-c", RUNNER, str(student)],
                              input=json.dumps(data, allow_nan=False), text=True,
                              capture_output=True, cwd=str(root), timeout=timeout)
    except subprocess.TimeoutExpired:
        raise ValueError("Student worker exceeded the five-second execution limit.")
    if len(proc.stdout.encode("utf-8")) > MAX_OUTPUT or len(proc.stderr.encode("utf-8")) > MAX_OUTPUT:
        raise ValueError("Student worker output exceeded the 64 KiB limit.")
    if proc.returncode:
        raise ValueError("Student worker failed (exit %s): %s" % (proc.returncode, proc.stderr[-1500:]))
    try:
        def reject_constant(value):
            raise ValueError("Non-finite JSON number: " + value)
        output = json.loads(proc.stdout, parse_constant=reject_constant)
    except (json.JSONDecodeError, ValueError):
        raise ValueError("Student worker must return one JSON-compatible object and print no extra output.")
    if not isinstance(output, dict):
        raise ValueError("Student worker must return a JSON object.")
    return output


def run(path):
    root, manifest = load_workspace(path)
    changed = preserved(root, manifest)
    if changed:
        raise ValueError("Baseline evidence changed: " + ", ".join(changed))
    data = json.loads(contained(root, "input.json").read_text(encoding="utf-8"))
    worker_hash = _hash(contained(root, "student.py"))
    input_hash = _hash(contained(root, "input.json"))
    try:
        output = invoke(root, data)
        changed = preserved(root, manifest)
        if changed:
            raise ValueError("Worker changed protected evidence: " + ", ".join(changed))
        if _hash(contained(root, "student.py")) != worker_hash:
            raise ValueError("Worker source changed during execution.")
    except ValueError as exc:
        failed = _record(root, "run", {
            "incident": manifest["incident"], "variant": manifest["variant"], "error": str(exc),
            "worker_sha256": worker_hash, "input_sha256": input_hash,
        })
        raise ValueError("%s Failure evidence retained in %s." % (exc, failed["record"]))
    result = {"incident": manifest["incident"], "variant": manifest["variant"], "output": output,
              "worker_sha256": worker_hash, "input_sha256": input_hash}
    return _record(root, "run", result)


def _schedule_issues(data, out):
    """Validate constraints, not a particular optimal schedule."""
    issues = []
    jobs = {j["id"]: j for j in data["jobs"]}
    schedule = out.get("schedule", [])
    deferred = out.get("deferred", [])
    if not isinstance(schedule, list) or not isinstance(deferred, list):
        return ["schedule/deferred must be arrays"]
    if type(out.get("spent")) is not int:
        issues.append("spent must be an integer")
    if any(type(job_id) is not str for job_id in deferred):
        return issues + ["deferred must contain job IDs"]
    try:
        ids = [row["id"] for row in schedule]
        if len(ids) != len(set(ids)) or len(deferred) != len(set(deferred)):
            issues.append("jobs must be accounted for exactly once")
        if set(ids) & set(deferred) or set(ids) | set(deferred) != set(jobs):
            issues.append("scheduled and deferred jobs must partition the input jobs")
        intervals, retries, spent = [], [], 0
        for row in schedule:
            job = jobs[row["id"]]
            start = row["start"]
            if type(start) is not int or start < max(job["arrival"], job["retry_after"]) \
                    or start + job["duration"] > data["deadline"]:
                issues.append("schedule violates an arrival, retry delay, or deadline")
            intervals.append((start, start + job["duration"]))
            if job["retry"]:
                retries.append(start)
            spent += job["cost"]
        if any(sum(a <= t < b for a, b in intervals) > data["max_concurrency"]
               for t in range(data["deadline"] + 1)):
            issues.append("schedule exceeds shared concurrency")
        if len(retries) != len(set(retries)):
            issues.append("retry jobs start in a synchronized burst")
        if spent != out.get("spent") or spent > data["budget"]:
            issues.append("shared budget accounting is invalid")
        feasible = any(job["cost"] <= data["budget"] and
                       max(job["arrival"], job["retry_after"]) + job["duration"] <= data["deadline"]
                       for job in jobs.values())
        if feasible and not schedule:
            issues.append("at least one feasible job must be admitted")
    except (KeyError, TypeError, ValueError):
        issues.append("schedule has an invalid record or unknown job")
    return issues


def _contract_equal(actual, expected, key=None):
    """JSON equality must not accept false as zero or absent as explicit null."""
    if expected is None:
        return actual is None
    if type(expected) is bool:
        return type(actual) is bool and actual == expected
    if isinstance(expected, (int, float)):
        if type(actual) not in (int, float):
            return False
        if key in {"checkpoint", "revision", "requirement_version"} and type(actual) is not int:
            return False
        try:
            return math.isfinite(actual) and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12)
        except OverflowError:
            return False
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            name in actual and _contract_equal(actual[name], value, name) for name, value in expected.items())
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) == len(expected) and all(
            _contract_equal(a, e) for a, e in zip(actual, expected))
    return type(actual) is type(expected) and actual == expected


def evaluate(case, data, output):
    from .reference import solve
    expected = solve(case, copy.deepcopy(data))
    issues = ["required field is missing: " + key for key in expected if key not in output]
    if case == "INC-05":
        issues.extend(_schedule_issues(data, output))
        fields = ("updates", "final_value")
    else:
        fields = expected.keys()
    for key in fields:
        if key in output and not _contract_equal(output[key], expected[key], key):
            issues.append("contract assertion failed for " + key)
    return issues


def _wrapper_checks(root):
    issues = []
    script = contained(root, "repository/tools/check.py")
    if not script.is_file():
        return ["repository test wrapper is missing"]
    # Compare to actual independent discovery, allowing the learner to add useful
    # feature tests without making the inherited three tests disappear.
    count_probe = (
        "import sys, unittest; sys.path.insert(0, sys.argv[1]); "
        "suite=unittest.defaultTestLoader.discover(sys.argv[1] + '/tests'); "
        "print(suite.countTestCases())"
    )
    discovery = subprocess.run(
        [sys.executable, "-I", "-c", count_probe, str(script.parent.parent)],
        cwd=str(root), capture_output=True, text=True, timeout=5,
    )
    try:
        actual_count = int(discovery.stdout.strip())
    except ValueError:
        actual_count = 0
    proc = subprocess.run([sys.executable, str(script)], cwd=str(root), capture_output=True, text=True, timeout=5)
    try:
        result = json.loads(proc.stdout)
        if proc.returncode or not isinstance(result, dict) \
                or type(result.get("discovered")) is not int or type(result.get("failures")) is not int \
                or actual_count < 3 or discovery.returncode \
                or result != {"discovered": actual_count, "failures": 0}:
            issues.append("repository wrapper does not accurately prove its passing tests from an unrelated cwd")
    except ValueError:
        issues.append("repository wrapper must print the specified JSON summary")
    feature = contained(root, "repository/report.py")
    if not feature.is_file():
        issues.append("requested feature module is missing")
    else:
        feature_probe = (
            "import sys; sys.path.insert(0, sys.argv[1]); "
            "from report import format_budget; "
            "assert format_budget(10, 3) == '7 remaining'; "
            "assert format_budget(10, 10) == '0 remaining'; "
            "assert format_budget(10, 11) == '0 remaining'; "
            "assert format_budget(0, 0) == '0 remaining'"
        )
        feature_run = subprocess.run([sys.executable, "-I", "-c", feature_probe, str(feature.parent)],
                                     cwd=str(root), capture_output=True, text=True, timeout=5)
        if feature_run.returncode:
            issues.append("requested feature fails its normal or boundary contract")
    with tempfile.TemporaryDirectory(prefix="incident-empty-tests-") as empty:
        tmp = Path(empty)
        (tmp / "tools").mkdir()
        (tmp / "tests").mkdir()
        (tmp / "empty_tests").mkdir()
        (tmp / "tools" / "check.py").write_bytes(script.read_bytes())
        empty_proc = subprocess.run([sys.executable, str(tmp / "tools" / "check.py")],
                                    cwd=str(tmp), capture_output=True, text=True, timeout=5)
        try:
            result = json.loads(empty_proc.stdout)
            if empty_proc.returncode == 0 or not isinstance(result, dict) \
                    or type(result.get("discovered")) is not int or type(result.get("failures")) is not int \
                    or result != {"discovered": 0, "failures": 0}:
                issues.append("repository wrapper does not fail on zero discovered tests")
        except ValueError:
            issues.append("empty-suite wrapper result is not valid JSON evidence")
        # A nonempty failure and a nonempty error must both produce a failing exit.
        # Use a new interpreter per probe to avoid retained test imports or caches.
        for label, body in (
            ("assertion", "self.assertEqual(1, 2)"),
            ("error", "raise RuntimeError('synthetic test infrastructure failure')"),
        ):
            (tmp / "tests" / "test_negative.py").write_text(
                "import unittest\nclass Negative(unittest.TestCase):\n"
                "    def test_case(self):\n        " + body + "\n", encoding="utf-8")
            negative = subprocess.run([sys.executable, "-B", str(tmp / "tools/check.py")],
                                      cwd=str(tmp), capture_output=True, text=True, timeout=5)
            try:
                result = json.loads(negative.stdout)
                valid_summary = isinstance(result, dict) and type(result.get("discovered")) is int \
                    and type(result.get("failures")) is int and result == {"discovered": 1, "failures": 1}
                if negative.returncode == 0 or not valid_summary:
                    issues.append("repository wrapper mishandles a nonempty %s failure" % label)
            except ValueError:
                issues.append("nonempty %s failure has no valid JSON evidence" % label)
    return issues


def check(path):
    root, manifest = load_workspace(path)
    case = manifest["incident"]
    failures = []
    changed = preserved(root, manifest)
    if changed:
        failures.append({"case": "evidence", "issues": ["protected evidence changed: " + ", ".join(changed)]})
        return _record(root, "check", {
            "incident": case, "workloads": 0, "passed": False, "failures": failures,
            "scope": "Execution stopped because baseline evidence changed.",
        })
    data = json.loads(contained(root, "input.json").read_text(encoding="utf-8"))
    worker_hash = _hash(contained(root, "student.py"))
    input_hash = _hash(contained(root, "input.json"))
    workloads = [("workspace", data)] + list(boundary_scenarios(case))
    executed = 0
    for name, workload in workloads:
        executed += 1
        try:
            issues = evaluate(case, workload, invoke(root, workload))
        except (ValueError, TypeError, KeyError) as exc:
            issues = [str(exc)]
        if issues:
            failures.append({"case": name, "issues": issues})
        if _hash(contained(root, "student.py")) != worker_hash or preserved(root, manifest):
            failures.append({"case": "integrity", "issues": ["source or protected evidence changed; further execution stopped"]})
            break
    if case == "INC-01":
        try:
            issues = _wrapper_checks(root)
        except subprocess.TimeoutExpired:
            issues = ["repository wrapper exceeded its five-second limit"]
        if issues:
            failures.append({"case": "repository", "issues": issues})
    changed = preserved(root, manifest)
    if changed and not any(f["case"] == "evidence" for f in failures):
        failures.append({"case": "evidence", "issues": ["worker changed protected evidence: " + ", ".join(changed)]})
    result = {"incident": case, "workloads": executed, "passed": not failures,
              "failures": failures, "worker_sha256": worker_hash, "input_sha256": input_hash,
              "scope": "Behavioral contracts and evidence preservation; human incident review still required."}
    return _record(root, "check", result)


def attempt(path, hypothesis, evidence_path, next_check):
    root, _ = load_workspace(path)
    if len(hypothesis.strip()) < 12 or len(next_check.strip()) < 12:
        raise ValueError("Write a specific hypothesis and next check (at least 12 characters each).")
    evidence_file = contained(root, evidence_path)
    if not evidence_file.is_file() or not evidence_file.stat().st_size:
        raise ValueError("Evidence must name an existing nonempty file inside this workspace.")
    attempts_path = contained(root, ".incident-attempts.json")
    attempts = json.loads(attempts_path.read_text(encoding="utf-8")) if attempts_path.exists() else []
    if not isinstance(attempts, list):
        raise ValueError("Attempt history is malformed; preserve it before repairing it.")
    record = {"hypothesis": hypothesis.strip(), "evidence": str(evidence_file.relative_to(root)),
              "evidence_sha256": _hash(evidence_file), "next_check": next_check.strip(),
              "at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    attempts.append(record)
    _json(attempts_path, attempts)
    return {"saved": True, "attempts": len(attempts), "guidance": "Available on explicit hint/debrief request; no answer was revealed."}


def guidance(path, level=None):
    root, manifest = load_workspace(path)
    history = contained(root, ".incident-attempts.json")
    attempts = json.loads(history.read_text(encoding="utf-8")) if history.exists() else []
    if not isinstance(attempts, list) or not any(
        isinstance(a, dict) and isinstance(a.get("hypothesis"), str)
        and isinstance(a.get("next_check"), str) and len(a["hypothesis"].strip()) >= 12
        and len(a["next_check"].strip()) >= 12 and a.get("evidence_sha256")
        for a in attempts
    ):
        raise ValueError("Save an evidence-backed attempt first. Guidance remains closed.")
    guidance_path = Path(__file__).resolve().parents[2] / "content" / "incidents.json"
    canonical = None
    if guidance_path.is_file():
        curriculum = json.loads(guidance_path.read_text(encoding="utf-8"))
        canonical = next((item for item in curriculum["incidents"] if item["id"] == manifest["incident"]), None)
    if level is not None:
        if level not in {1, 2, 3}:
            raise ValueError("Hint level must be 1, 2, or 3.")
        hints = [
            "Choose one apparent success. Which current, authoritative evidence would make it trustworthy?",
            "Trace scope, time, and version through the input. Identify one observation that would distinguish your two strongest hypotheses.",
            "Turn each CONTRACT.md condition into a small predicate. Exercise both its acceptance and refusal boundary before combining them.",
        ]
        result = {"incident": manifest["incident"], "level": level,
                  "hint": canonical["hints"][level - 1] if canonical else hints[level - 1]}
        if level == 3:
            from .reference import DETAILED_CONTRACTS
            result["worked_constraints"] = DETAILED_CONTRACTS[manifest["incident"]]
        return result
    from .reference import DEBRIEFS
    return {"incident": manifest["incident"], "debrief": canonical["debrief"] if canonical else DEBRIEFS[manifest["incident"]],
            "next": "Explain why a plausible competing diagnosis was rejected, then create a new workspace with --variant transfer."}
