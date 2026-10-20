"""Your workspace. TODOs are intentional; the reference harness never imports this.

Run: python3 -m lab.cli practice --lab 01
Then compose all eight: python3 -m lab.composed evaluate --components student
Hints and solutions are separate files under content/labs/.
"""


def redact_sensitive(text):
    """Lab 01: replace email addresses with [EMAIL] and sk-demo-* keys with [KEY]."""
    raise NotImplementedError("Complete lab 01.")


def pack_context(articles, max_chars):
    """Lab 02: return article IDs ranked by descending relevance, then ID.

    Charge len(article['text']); skip articles that do not fit, preserving rank.
    Include a given ID at most once. Reject negative budgets.
    """
    raise NotImplementedError("Complete lab 02.")


def tool_allowed(name, arguments, allowed_tools, ticket_id):
    """Lab 03: bool; allow only well-formed read_ticket for the authorized ticket.

    No optional or additional keys. A string ticket ID must match exactly.
    """
    raise NotImplementedError("Complete lab 03.")


def retry_delay_ms(attempt, base_ms, cap_ms):
    """Lab 04: capped exponential backoff; attempt starts at zero.

    Reject negative/noninteger inputs (including booleans).
    """
    raise NotImplementedError("Complete lab 04.")


def operation_key(run_id, ticket_id, action):
    """Lab 05: stable nonempty string <=160 chars; avoid delimiter collisions."""
    raise NotImplementedError("Complete lab 05.")


def citations_valid(citations, retrieved):
    """Lab 06: bool; nonempty unique string IDs, all present in retrieved IDs."""
    raise NotImplementedError("Complete lab 06.")


def summarize_trace(events):
    """Lab 07: return tool_attempts, rejections, retries, replay_hits integer counts."""
    raise NotImplementedError("Complete lab 07.")


def build_decision(ticket, articles):
    """Lab 08: produce the decision contract used by lab.policy.validate_decision.

    This extension is opt-in: evaluate --policy student (decision only), or
    lab.composed evaluate --components student (all eight helpers). You may import classify
    from lab.policy; focus on grounding, conservative escalation and output schema.
    """
    raise NotImplementedError("Complete lab 08.")
