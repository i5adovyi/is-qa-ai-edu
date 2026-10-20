"""Small, strict tool contracts. No code execution, network, or provider SDKs."""

from dataclasses import asdict, dataclass
from typing import Any
import re


class HarnessError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class SimulatedCrash(HarnessError):
    """Deliberately stops a run after a durable write and before its acknowledgment."""


TOOL_SCHEMAS = {
    "read_ticket": {
        "description": "Read one synthetic ticket belonging to this run.",
        "required": {"ticket_id": "string"},
        "optional": {},
        "mutation": False,
    },
    "search_kb": {
        "description": "Return approved knowledge for one topic.",
        "required": {"topic": "string"},
        "optional": {},
        "mutation": False,
    },
    "save_draft": {
        "description": "Save a local draft only. Never send it.",
        "required": {"ticket_id": "string", "reply": "string", "citations": "strings"},
        "optional": {},
        "mutation": True,
    },
    "add_tag": {
        "description": "Tag one ticket. Requires a ticket-specific approval grant.",
        "required": {"ticket_id": "string", "tag": "string"},
        "optional": {},
        "mutation": True,
    },
}

DEFAULT_ALLOWLIST = frozenset({"read_ticket", "search_kb", "save_draft", "add_tag"})
TOPICS = frozenset({"billing", "access", "export", "incident", "unknown", "safety"})
TAGS = frozenset({"triaged", "needs_review"})


def validate_arguments(name: str, arguments: Any) -> None:
    if name not in TOOL_SCHEMAS:
        raise HarnessError("unknown_tool", f"Unknown tool: {name}")
    if type(arguments) is not dict:
        raise HarnessError("invalid_arguments", "Arguments must be an object.")
    schema = TOOL_SCHEMAS[name]
    required = schema["required"]
    if set(arguments) != set(required):
        raise HarnessError("invalid_arguments", "Missing or additional arguments.")
    for key, expected in required.items():
        value = arguments[key]
        if expected == "string" and (type(value) is not str or not value.strip()):
            raise HarnessError("invalid_arguments", f"{key} must be a nonempty string.")
        if expected == "strings" and (
            type(value) is not list
            or any(type(item) is not str or not item for item in value)
            or len(value) != len(set(value))
        ):
            raise HarnessError("invalid_arguments", f"{key} must be unique strings.")
    if name == "read_ticket" or "ticket_id" in arguments:
        if not re.fullmatch(r"T-[0-9]{3}", arguments["ticket_id"]):
            raise HarnessError("invalid_arguments", "Invalid ticket identifier.")
    if name == "search_kb" and arguments["topic"] not in TOPICS:
        raise HarnessError("invalid_arguments", "Topic is outside the controlled vocabulary.")
    if name == "add_tag" and arguments["tag"] not in TAGS:
        raise HarnessError("invalid_arguments", "Tag is outside the controlled vocabulary.")
    if name == "save_draft":
        if len(arguments["reply"]) > 4000 or len(arguments["citations"]) > 4:
            raise HarnessError("invalid_arguments", "Draft exceeds the contract.")


@dataclass
class Budget:
    max_steps: int = 14
    max_tool_calls: int = 8
    max_context_chars: int = 16000
    max_virtual_ms: int = 1000

    def __post_init__(self):
        if any(type(value) is not int or value < 1 for value in asdict(self).values()):
            raise ValueError("Budget limits must be positive integers.")


@dataclass
class Usage:
    steps: int = 0
    tool_calls: int = 0
    context_chars: int = 0
    virtual_ms: int = 0

    def __post_init__(self):
        if any(type(value) is not int or value < 0 for value in asdict(self).values()):
            raise ValueError("Usage counters must be nonnegative integers.")

    def consume(self, budget: Budget, field: str, amount: int = 1):
        if type(amount) is not int or amount < 0:
            raise ValueError("Consumption must be a nonnegative integer.")
        if field not in asdict(self):
            raise ValueError("Unknown budget dimension.")
        # Charge attempted work even when the attempt crosses the boundary.
        setattr(self, field, getattr(self, field) + amount)
        if getattr(self, field) > getattr(budget, "max_" + field):
            raise HarnessError("budget_exhausted", f"{field} budget exhausted.")
