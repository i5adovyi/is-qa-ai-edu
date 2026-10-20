"""Policy enforcement lives outside the policy/model."""

import json
from pathlib import Path

from .contracts import DEFAULT_ALLOWLIST, HarnessError, validate_arguments
from .storage import digest


DATA_DIR = Path(__file__).parent / "data"


def load_knowledge():
    return json.loads((DATA_DIR / "knowledge.json").read_text(encoding="utf-8"))


class Dispatcher:
    def __init__(self, store, trace, budget, usage, ticket_id, allowlist=None,
                 approvals=None, knowledge=None, fault_state=None):
        self.store = store
        self.trace = trace
        self.budget = budget
        self.usage = usage
        self.ticket_id = ticket_id
        if store.data["ticket"].get("id") != ticket_id:
            raise HarnessError("scope_denied", "Store ticket does not match the authorized scope.")
        self.allowlist = DEFAULT_ALLOWLIST if allowlist is None else frozenset(allowlist)
        self.approvals = frozenset(approvals or ())
        self.knowledge = load_knowledge() if knowledge is None else knowledge
        self.fault_state = fault_state if fault_state is not None else {}
        self.retrieved_ids = set()

    def call(self, name, arguments, key=None):
        # Trace bounded metadata, never untrusted bodies, reply text, or tool secrets.
        self.trace.emit("tool_attempt", tool=name,
                        argument_keys=sorted(arguments) if isinstance(arguments, dict) else [],
                        request_hash=digest({"tool": name, "arguments": arguments}),
                        idempotency_key=key)
        try:
            self.usage.consume(self.budget, "tool_calls")
            if name not in self.allowlist:
                raise HarnessError("tool_denied", "Tool is outside this run's allowlist.")
            validate_arguments(name, arguments)
            if "ticket_id" in arguments and arguments["ticket_id"] != self.ticket_id:
                raise HarnessError("scope_denied", "Ticket is outside this run's scope.")
            if name == "add_tag" and f"tag:{self.ticket_id}" not in self.approvals:
                raise HarnessError("approval_required", "Ticket-specific tag approval is required.")
            self.usage.consume(self.budget, "virtual_ms", 20)
            if name == "search_kb" and self.fault_state.get("timeouts_remaining", 0):
                self.fault_state["timeouts_remaining"] -= 1
                self.usage.consume(self.budget, "virtual_ms", 100)
                raise HarnessError("tool_timeout", "Synthetic retrieval timeout.")
            if name == "read_ticket":
                result = dict(self.store.data["ticket"])
            elif name == "search_kb":
                result = [item for item in self.knowledge if item["topic"] == arguments["topic"]]
            elif name == "save_draft":
                valid_ids = {item["id"] for item in self.knowledge}
                citations = set(arguments["citations"])
                if not citations or not citations <= (valid_ids & self.retrieved_ids):
                    raise HarnessError("unsupported_citation", "Citations must be retrieved in this run.")
                result = self.store.mutate(name, arguments, key)
                self.trace.emit("mutation_committed", tool=name, replayed=result["replayed"],
                                idempotency_key=key)
            else:
                result = self.store.mutate(name, arguments, key)
                self.trace.emit("mutation_committed", tool=name, replayed=result["replayed"],
                                idempotency_key=key)
            # Budget tool output BEFORE exposing it to the policy.
            self.usage.consume(self.budget, "context_chars", len(json.dumps(result)))
            if name == "search_kb":
                self.retrieved_ids.update(item["id"] for item in result)
            self.trace.emit("tool_result", tool=name, result_hash=digest(result),
                            replayed=result.get("replayed", False) if isinstance(result, dict) else False)
            return result
        except HarnessError as exc:
            self.trace.emit("tool_rejected", tool=name, code=exc.code)
            raise
