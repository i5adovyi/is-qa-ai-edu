"""Spoilers: one possible implementation of all eight public lab contracts.

Do not replace the whole student module unless you want to skip the exercises.
These functions are deliberately small. Passing public checks is a starting point,
not evidence that a redactor, context selector or policy is ready for production.
"""

import hashlib
import json
import re

from lab.policy import classify


def redact_sensitive(text):
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL]", text)
    return re.sub(r"\bsk-demo-[A-Za-z0-9_-]+", "[KEY]", text)


def pack_context(articles, max_chars):
    if max_chars < 0:
        raise ValueError("Negative context budget.")
    ranked = sorted(articles, key=lambda item: (-item["relevance"], item["id"]))
    selected, used, seen = [], 0, set()
    for article in ranked:
        if article["id"] in seen:
            continue
        # Duplicate IDs have one canonical ranked representative.
        seen.add(article["id"])
        if used + len(article["text"]) <= max_chars:
            selected.append(article["id"])
            used += len(article["text"])
    return selected


def tool_allowed(name, arguments, allowed_tools, ticket_id):
    return (
        name == "read_ticket" and name in allowed_tools
        and type(arguments) is dict and set(arguments) == {"ticket_id"}
        and type(arguments["ticket_id"]) is str
        and arguments["ticket_id"] == ticket_id
    )


def retry_delay_ms(attempt, base_ms, cap_ms):
    if any(type(value) is not int or value < 0 for value in (attempt, base_ms, cap_ms)):
        raise ValueError("Require nonnegative integers.")
    if base_ms == 0:
        return 0
    # Avoid huge integer allocation for an attacker-controlled attempt number.
    if attempt >= cap_ms.bit_length():
        return cap_ms
    return min(cap_ms, base_ms * (2 ** attempt))


def operation_key(run_id, ticket_id, action):
    canonical = json.dumps([run_id, ticket_id, action], separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def citations_valid(citations, retrieved):
    return (
        type(citations) is list and bool(citations)
        and all(type(value) is str and bool(value) for value in citations)
        and len(citations) == len(set(citations))
        and set(citations) <= set(retrieved)
    )


def summarize_trace(events):
    return {
        "tool_attempts": sum(event.get("event") == "tool_attempt" for event in events),
        "rejections": sum(event.get("event") == "tool_rejected" for event in events),
        "retries": sum(event.get("event") == "retry_scheduled" for event in events),
        "replay_hits": sum(event.get("event") == "tool_result" and event.get("replayed") is True
                           for event in events),
    }


def build_decision(ticket, articles):
    category = classify(ticket)
    relevant = [article for article in articles if article["topic"] == category]
    if category in {"safety", "unknown"} or len(relevant) != 1:
        return {
            "action": "escalate", "category": category, "reply": "", "citations": [],
            "reason": "The request needs human review or lacks unambiguous evidence.",
        }
    article = relevant[0]
    return {
        "action": "draft", "category": category, "reply": article["answer"],
        "citations": [article["id"]], "reason": "The approved article supports this draft.",
    }
