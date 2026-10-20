"""Transparent mock policy. This is deliberately NOT an LLM or injection detector."""

import re

from .contracts import HarnessError, TOPICS


INJECTION_PATTERNS = (
    r"ignore (?:all |previous |the )*(?:instructions|rules)",
    r"(?:reveal|print|send|upload|exfiltrate).{0,50}(?:secret|api.key|password|token)",
    r"system (?:message|prompt|override)",
    r"(?:run|execute) (?:this |a )?(?:shell|command|script)",
    r"disable (?:the )?(?:guard|safety|allowlist)",
    r"you are now",
)


def classify(ticket):
    text = f"{ticket['subject']} {ticket['body']}".lower()
    if any(re.search(pattern, text, flags=re.S) for pattern in INJECTION_PATTERNS):
        return "safety"
    groups = [
        ("incident", ("outage", "service down", "503", "unavailable")),
        ("billing", ("refund", "charged twice", "duplicate charge", "billing", "invoice")),
        ("access", ("password", "log in", "login", "locked out", "sign in")),
        ("export", ("export", "download my data", "csv")),
    ]
    matches = [topic for topic, words in groups if any(word in text for word in words)]
    # Ambiguous requests require a human; ordering must not silently decide.
    return matches[0] if len(matches) == 1 else "unknown"


def decide(ticket, articles):
    category = classify(ticket)
    if category == "safety":
        return {
            "action": "escalate", "category": category, "citations": [],
            "reply": "", "reason": "Untrusted content contains instruction-like text.",
        }
    if category == "unknown" or len(articles) != 1:
        return {
            "action": "escalate", "category": category, "citations": [],
            "reply": "", "reason": "Insufficient or ambiguous approved evidence.",
        }
    article = articles[0]
    return {
        "action": "draft",
        "category": category,
        "reply": article["answer"],
        "citations": [article["id"]],
        "reason": "One relevant approved knowledge article supports this local draft.",
    }


def validate_decision(decision, articles):
    required = {"action", "category", "reply", "citations", "reason"}
    if type(decision) is not dict or set(decision) != required:
        raise HarnessError("invalid_decision", "Decision has an invalid structure.")
    if type(decision["action"]) is not str or decision["action"] not in {"draft", "escalate"}:
        raise HarnessError("invalid_decision", "Unsupported decision action.")
    if type(decision["category"]) is not str or decision["category"] not in TOPICS:
        raise HarnessError("invalid_decision", "Unsupported decision category.")
    if type(decision["reply"]) is not str or type(decision["reason"]) is not str:
        raise HarnessError("invalid_decision", "Decision text must be strings.")
    if type(decision["citations"]) is not list or any(
        type(value) is not str for value in decision["citations"]
    ):
        raise HarnessError("invalid_decision", "Citations must be a list of strings.")
    if len(decision["citations"]) != len(set(decision["citations"])):
        raise HarnessError("invalid_decision", "Citations must be unique.")
    if len(decision["reply"]) > 4000 or len(decision["reason"]) > 1000:
        raise HarnessError("invalid_decision", "Decision exceeds the output contract.")
    relevant = {article["id"] for article in articles if article["topic"] == decision["category"]}
    if decision["action"] == "draft":
        if not decision["reply"] or not decision["citations"] or not set(decision["citations"]) <= relevant:
            raise HarnessError("unsupported_citation", "Draft must cite retrieved, relevant evidence.")
    elif decision["reply"] or decision["citations"]:
        raise HarnessError("invalid_decision", "Escalations must not contain an automatic draft.")
