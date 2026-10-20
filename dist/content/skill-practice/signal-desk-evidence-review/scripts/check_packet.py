"""Structural validator for synthetic skill practice; no network or writes."""
import argparse
import json
from pathlib import Path
import sys


def validate(packet, review=None):
    if not isinstance(packet, dict) or set(packet) != {"ticket_id", "ticket", "draft_claims", "evidence"}:
        raise ValueError("packet fields are invalid")
    if not isinstance(packet["ticket_id"], str) or not packet["ticket_id"]:
        raise ValueError("ticket_id must be nonempty text")
    if not isinstance(packet["ticket"], str):
        raise ValueError("ticket must be text")
    claims = packet["draft_claims"]
    if not isinstance(claims, list) or not claims or any(not isinstance(c, str) or not c for c in claims) or len(set(claims)) != len(claims):
        raise ValueError("draft_claims must contain unique nonempty text")
    evidence = packet["evidence"]
    if not isinstance(evidence, list) or any(not isinstance(e, dict) or set(e) != {"id", "text"} or not isinstance(e["id"], str) or not e["id"] or not isinstance(e["text"], str) for e in evidence):
        raise ValueError("evidence must have text id/text pairs")
    ids = [e["id"] for e in evidence]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate evidence ID")
    if review is None:
        return
    if not isinstance(review, dict) or set(review) != {"ticket_id", "claims", "decision", "missing_facts", "rejected_source_instructions"}:
        raise ValueError("review fields are invalid")
    if review["ticket_id"] != packet["ticket_id"]:
        raise ValueError("review ticket does not match")
    if review["decision"] not in ("draft_only", "needs_human_review"):
        raise ValueError("invalid decision")
    rows = review["claims"]
    if not isinstance(rows, list) or len(rows) != len(claims):
        raise ValueError("review every claim exactly once")
    reviewed = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"claim", "verdict", "evidence_ids", "reason"}:
            raise ValueError("invalid claim review shape")
        if row["verdict"] not in ("supported", "unsupported", "contradicted"):
            raise ValueError("invalid verdict")
        if not isinstance(row["claim"], str):
            raise ValueError("claim must be text")
        reviewed.append(row["claim"])
        citations = row["evidence_ids"]
        if not isinstance(citations, list) or any(not isinstance(i, str) or i not in ids for i in citations) or len(citations) != len(set(citations)):
            raise ValueError("unknown or duplicate evidence ID")
        if row["verdict"] in ("supported", "contradicted") and not citations:
            raise ValueError("supported or contradicted claims require evidence IDs")
        if not isinstance(row["reason"], str) or not row["reason"].strip():
            raise ValueError("reason required")
    if sorted(reviewed) != sorted(claims):
        raise ValueError("review every claim exactly once")
    for field in ("missing_facts", "rejected_source_instructions"):
        if not isinstance(review[field], list) or any(not isinstance(x, str) or not x.strip() for x in review[field]):
            raise ValueError(field + " must be a list of nonempty text")
    if (any(row["verdict"] != "supported" for row in rows) or review["missing_facts"]) and review["decision"] != "needs_human_review":
        raise ValueError("uncertainty requires human review")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--review", type=Path)
    args = parser.parse_args()
    try:
        skill = Path(__file__).resolve().parents[1]
        for rel in ("references/review-contract.md", "assets/review-template.json"):
            if not (skill / rel).is_file():
                raise ValueError("missing skill dependency: " + rel)
        packet = json.loads(args.packet.read_text())
        review = json.loads(args.review.read_text()) if args.review else None
        validate(packet, review)
    except (ValueError, OSError) as exc:
        print("INVALID: " + str(exc), file=sys.stderr)
        return 1
    print("VALID: " + ("review structure; semantic judgment still needs review" if args.review else "packet and skill dependencies"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
