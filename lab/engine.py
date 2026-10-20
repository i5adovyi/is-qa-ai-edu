"""A checkpointed read → retrieve → decide → draft state machine."""

from dataclasses import asdict
from copy import deepcopy
from pathlib import Path
import json
import uuid

from .contracts import Budget, HarnessError, SimulatedCrash, Usage
from .policy import classify, decide, validate_decision
from .storage import Store, Trace, atomic_json, digest
from .tools import Dispatcher, DATA_DIR


SCENARIOS = (
    "normal", "injection", "timeout-once", "timeout-always", "invalid-tool",
    "budget", "duplicate", "crash-after-write", "denied-tag", "approved-tag",
    "context-overflow",
)


def load_cases(split="all"):
    cases = json.loads((DATA_DIR / "cases.json").read_text(encoding="utf-8"))
    return [case for case in cases if split == "all" or case["split"] == split]


def get_case(case_id):
    for case in load_cases():
        if case["id"] == case_id:
            return case
    raise HarnessError("unknown_case", f"Unknown case {case_id}.")


def validate_checkpoint_state(state, run_id):
    """Checks shape, not authenticity; local files remain trusted input."""
    expected = {"phase", "scenario", "case_id", "ticket_id", "ticket", "articles",
                "decision", "result", "retries", "faults", "crash_armed"}
    if type(state) is not dict or set(state) != expected:
        raise HarnessError("checkpoint_corrupt", "Invalid checkpoint state fields.")
    if (
        type(run_id) is not str or not run_id
        or type(state["phase"]) is not str
        or state["phase"] not in {"read", "retrieve", "decide", "save", "tag", "finish", "done"}
        or type(state["scenario"]) is not str or state["scenario"] not in SCENARIOS
        or type(state["case_id"]) is not str or type(state["ticket_id"]) is not str
        or type(state["retries"]) is not int or not 0 <= state["retries"] <= 1
        or type(state["crash_armed"]) is not bool
        or type(state["faults"]) is not dict
        or set(state["faults"]) != {"timeouts_remaining"}
        or type(state["faults"]["timeouts_remaining"]) is not int
        or state["faults"]["timeouts_remaining"] < 0
    ):
        raise HarnessError("checkpoint_corrupt", "Invalid checkpoint phase or counters.")
    if type(state["articles"]) is not list or any(
        type(article) is not dict
        or any(type(article.get(key)) is not str for key in ("id", "topic", "answer"))
        for article in state["articles"]
    ):
        raise HarnessError("checkpoint_corrupt", "Invalid checkpoint evidence.")
    if state["ticket"] is not None and (
        type(state["ticket"]) is not dict
        or any(type(state["ticket"].get(key)) is not str for key in ("id", "subject", "body"))
        or state["ticket"]["id"] != state["ticket_id"]
    ):
        raise HarnessError("checkpoint_corrupt", "Invalid checkpoint ticket.")
    if state["phase"] not in {"read", "done"} and state["ticket"] is None:
        raise HarnessError("checkpoint_corrupt", "Missing observed ticket.")
    if state["decision"] is not None:
        try:
            validate_decision(state["decision"], state["articles"])
        except HarnessError as exc:
            raise HarnessError("checkpoint_corrupt", "Invalid checkpoint decision.") from exc
    if state["phase"] in {"save", "tag", "finish"} and (
        state["decision"] is None or state["decision"]["action"] != "draft"
    ):
        raise HarnessError("checkpoint_corrupt", "Missing pending draft decision.")
    if state["phase"] == "done":
        result = state["result"]
        result_fields = {"run_id", "case_id", "status", "error", "decision", "usage",
                         "draft_count", "writes", "tags"}
        if (type(result) is not dict or set(result) != result_fields
                or result["run_id"] != run_id or result["case_id"] != state["case_id"]
                or type(result["status"]) is not str
                or result["status"] not in {"completed", "failed", "escalated"}):
            raise HarnessError("checkpoint_corrupt", "Invalid completed result.")


class Runner:
    def __init__(self, run_dir, case=None, scenario="normal", resume=False,
                 policy=None, budget=None, binding=None):
        self.run_dir = Path(run_dir)
        self.checkpoint_path = self.run_dir / "checkpoint.json"
        self.policy = decide if policy is None else policy
        self.binding = binding
        if resume:
            try:
                envelope = json.loads(self.checkpoint_path.read_text(encoding="utf-8"))
                if type(envelope) is not dict:
                    raise HarnessError("checkpoint_corrupt", "Checkpoint must be an object.")
                payload = envelope["payload"]
                if type(payload) is not dict:
                    raise HarnessError("checkpoint_corrupt", "Checkpoint payload must be an object.")
                if envelope.get("sha256") != digest(payload):
                    raise HarnessError("checkpoint_corrupt", "Checkpoint checksum mismatch.")
                if payload.get("version") != 1:
                    raise HarnessError("checkpoint_version", "Unsupported checkpoint version.")
                if payload.get("binding") != self.binding:
                    raise HarnessError("component_mismatch", "Resume requires the original component profile and source.")
                self.state = payload["state"]
                self.budget = Budget(**payload["budget"])
                self.usage = Usage(**payload["usage"])
                self.run_id = payload["run_id"]
                validate_checkpoint_state(self.state, self.run_id)
            except (KeyError, ValueError, TypeError, OSError) as exc:
                raise HarnessError("checkpoint_corrupt", "Checkpoint could not be loaded.") from exc
            self.store = Store(self.run_dir / "store.json", run_id=self.run_id)
        else:
            if scenario not in SCENARIOS:
                raise ValueError("Unsupported scenario.")
            if case is None:
                case = get_case("train-01")
            if scenario == "injection":
                case = get_case("train-13")
            if self.run_dir.exists() and any(self.run_dir.iterdir()):
                raise HarnessError("run_exists", "Use a fresh run directory or resume its checkpoint.")
            self.run_id = uuid.uuid4().hex[:12]
            self.budget = budget or Budget()
            if scenario == "budget" and budget is None:
                self.budget = Budget(max_tool_calls=1)
            if scenario == "context-overflow" and budget is None:
                self.budget = Budget(max_context_chars=30)
            self.usage = Usage()
            self.state = {
                "phase": "read", "scenario": scenario, "case_id": case["id"],
                "ticket_id": case["ticket"]["id"], "ticket": None, "articles": [],
                "decision": None, "result": None, "retries": 0,
                "faults": {"timeouts_remaining": 1 if scenario == "timeout-once"
                           else 10 if scenario == "timeout-always" else 0},
                "crash_armed": scenario == "crash-after-write",
            }
            self.store = Store(self.run_dir / "store.json", case["ticket"], run_id=self.run_id)
        self.trace = Trace(self.run_dir / "trace.jsonl", self.run_id)
        approvals = ([f"tag:{self.state['ticket_id']}"]
                     if self.state["scenario"] == "approved-tag" else [])
        self.dispatcher = Dispatcher(
            self.store, self.trace, self.budget, self.usage,
            self.state["ticket_id"], approvals=approvals, fault_state=self.state["faults"],
        )
        self.dispatcher.retrieved_ids = {article["id"] for article in self.state["articles"]}
        if not (resume and self.state["phase"] == "done"):
            self.trace.emit("run_resumed" if resume else "run_started",
                            scenario=self.state["scenario"], case_id=self.state["case_id"],
                            limits=asdict(self.budget), phase=self.state["phase"])
            self.checkpoint()

    def checkpoint(self):
        payload = {
            "version": 1, "run_id": self.run_id, "state": self.state,
            "budget": asdict(self.budget), "usage": asdict(self.usage),
            "binding": self.binding,
        }
        atomic_json(self.checkpoint_path, {"payload": payload, "sha256": digest(payload)})

    def _read_ticket(self):
        return self.dispatcher.call("read_ticket", {"ticket_id": self.state["ticket_id"]})

    def _prepare_articles(self, articles):
        return articles

    def _validate_decision(self, decision):
        validate_decision(decision, self.state["articles"])

    def _operation_key(self, action):
        return f"{self.run_id}:{action}:{self.state['ticket_id']}"

    def _retry_delay(self, attempt):
        return 0

    def _complete(self, status, code=None):
        self.state["phase"] = "done"
        self.state["result"] = {
            "run_id": self.run_id, "case_id": self.state["case_id"],
            "status": status, "error": code, "decision": self.state["decision"],
            "usage": asdict(self.usage), "draft_count": len(self.store.data["drafts"]),
            "writes": self.store.data["writes"], "tags": self.store.data["tags"],
        }
        self.trace.emit("run_completed", status=status, code=code, usage=asdict(self.usage))
        self.checkpoint()
        atomic_json(self.run_dir / "result.json", self.state["result"])
        return self.state["result"]

    def run(self):
        if self.state["phase"] == "done":
            return self.state["result"]
        while True:
            phase = self.state["phase"]
            try:
                self.usage.consume(self.budget, "steps")
                self.trace.emit("phase_started", phase=phase)
                if phase == "read":
                    self.state["ticket"] = self._read_ticket()
                    self.state["phase"] = "retrieve"
                elif phase == "retrieve":
                    if self.state["scenario"] == "invalid-tool":
                        self.dispatcher.call("run_shell", {"command": "echo unsafe"})
                    topic = classify(self.state["ticket"])
                    self.state["articles"] = self._prepare_articles(
                        self.dispatcher.call("search_kb", {"topic": topic}))
                    self.state["phase"] = "decide"
                elif phase == "decide":
                    try:
                        decision = self.policy(deepcopy(self.state["ticket"]),
                                               deepcopy(self.state["articles"]))
                    except Exception as exc:
                        raise HarnessError("policy_error", f"Policy failed: {type(exc).__name__}.") from exc
                    self._validate_decision(decision)
                    self.state["decision"] = decision
                    self.trace.emit("decision", action=decision["action"],
                                    category=decision["category"], citations=decision["citations"])
                    if decision["action"] == "escalate":
                        return self._complete("escalated")
                    self.state["phase"] = "save"
                elif phase == "save":
                    arguments = {
                        "ticket_id": self.state["ticket_id"],
                        "reply": self.state["decision"]["reply"],
                        "citations": self.state["decision"]["citations"],
                    }
                    key = self._operation_key("draft")
                    should_crash = self.state["crash_armed"]
                    # Persist intent and disarm synthetic crash before committing.
                    self.state["crash_armed"] = False
                    self.checkpoint()
                    self.dispatcher.call("save_draft", arguments, key=key)
                    if should_crash:
                        self.trace.emit("simulated_crash", phase=phase, after_commit=True)
                        # Preserve consumed budget, but leave pending intent in phase=save.
                        self.checkpoint()
                        raise SimulatedCrash("simulated_crash", "Write committed; resume its checkpoint.")
                    if self.state["scenario"] == "duplicate":
                        self.dispatcher.call("save_draft", arguments, key=key)
                    self.state["phase"] = ("tag" if self.state["scenario"]
                                           in {"denied-tag", "approved-tag"} else "finish")
                elif phase == "tag":
                    self.dispatcher.call(
                        "add_tag", {"ticket_id": self.state["ticket_id"], "tag": "triaged"},
                        key=self._operation_key("tag"),
                    )
                    self.state["phase"] = "finish"
                elif phase == "finish":
                    return self._complete("completed")
                else:
                    raise HarnessError("invalid_phase", "Unknown checkpoint phase.")
                self.checkpoint()
            except SimulatedCrash:
                raise
            except HarnessError as exc:
                if exc.code == "tool_timeout" and self.state["retries"] < 1:
                    try:
                        delay_ms = self._retry_delay(self.state["retries"])
                        self.usage.consume(self.budget, "virtual_ms", delay_ms)
                    except HarnessError as retry_error:
                        return self._complete("failed", retry_error.code)
                    self.state["retries"] += 1
                    self.trace.emit("retry_scheduled", phase=phase,
                                    retry=self.state["retries"], cause=exc.code, delay_ms=delay_ms)
                    self.checkpoint()
                    continue
                return self._complete("failed", exc.code)
