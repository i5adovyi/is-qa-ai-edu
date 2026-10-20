"""Versioned lexical/hybrid retrieval comparison with independently labeled cases."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "content/practice-corpus/retrieval.json"
CONCEPTS = [
    {"download", "export", "extract"},
    {"login", "authentication", "signin", "access"},
    {"invoice", "charge", "billing", "payment"},
    {"duplicate", "twice", "double"},
    {"large", "oversized", "huge"},
    {"reset", "expired", "expiration"},
]
STOP = {"a", "an", "the", "my", "is", "to", "for", "in", "of", "and", "it", "on", "with"}


def terms(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP


def expanded(words):
    result = set(words)
    for group in CONCEPTS:
        if words & group:
            result.update(group)
    return result


def retrieve(query, records, mode="lexical", version=None, k=3):
    """No label access. Hybrid here means lexical + explicit synonym expansion."""
    if mode not in {"lexical", "hybrid"} or type(k) is not int or k < 1:
        raise ValueError("invalid retrieval configuration")
    q = terms(query)
    scored = []
    seen = set()
    for record in records:
        if record["id"] in seen:
            raise ValueError("duplicate record ID")
        seen.add(record["id"])
        if version is not None and record["version"] not in {version, "all"}:
            continue
        words = terms(record["title"] + " " + record["text"])
        score = len(q & words)
        if mode == "hybrid":
            score = score * 2 + len(expanded(q) & expanded(words))
        if score:
            scored.append((score, record["id"]))
    return [rid for _, rid in sorted(scored, key=lambda item: (-item[0], item[1]))[:k]]


def claim_support(claims, retrieved, records):
    """Explicit classroom claim IDs, not a natural-language entailment model."""
    by_id = {r["id"]: r for r in records}
    labels = []
    for claim in claims:
        source = by_id.get(claim["source_id"])
        if source is None or source["id"] not in retrieved:
            verdict = "not_retrieved"
        elif claim["claim_id"] in source.get("supports", []):
            verdict = "supported"
        elif claim["claim_id"] in source.get("contradicts", []):
            verdict = "contradicted"
        else:
            verdict = "not_established"
        labels.append({"claim": claim, "verdict": verdict})
    return labels


def evaluate(data, mode, metadata=True, k=3):
    results = []
    for case in data["cases"]:
        ids = retrieve(case["query"], data["records"], mode,
                       case["version"] if metadata else None, k)
        required = set(case["required"])
        found = required & set(ids)
        claims = claim_support(case.get("candidate_claims", []), ids, data["records"])
        results.append({
            "id": case["id"], "tags": case["tags"], "retrieved": ids,
            "required": sorted(required), "recall_at_k": len(found) / len(required) if required else None,
            "no_answer_case": not required,
            "no_answer_has_matches": bool(ids) if not required else None,
            "claim_checks": claims,
        })
    answerable = [x for x in results if x["recall_at_k"] is not None]
    return {
        "mode": mode, "metadata_filter": metadata, "k": k,
        "cases": results, "answerable_count": len(answerable),
        "macro_recall": sum(x["recall_at_k"] for x in answerable) / len(answerable) if answerable else None,
        "claim_verdicts": dict(Counter(c["verdict"] for x in results for c in x["claim_checks"])),
        "limitations": "Fixed synthetic labels; synonym hybrid, not embeddings. Claim IDs are authored labels, not semantic inference. Search matches do not establish answerability.",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corpus", type=Path, default=CORPUS)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    raw = args.corpus.read_bytes()
    data = json.loads(raw)
    args.out.mkdir(parents=True, exist_ok=False)
    variants = [evaluate(data, "lexical"), evaluate(data, "hybrid"),
                evaluate(data, "hybrid", metadata=False)]
    base, candidate = variants[:2]
    comparisons = [{"id": a["id"], "baseline": a["recall_at_k"], "candidate": b["recall_at_k"],
                    "changed_ids": a["retrieved"] != b["retrieved"]}
                   for a, b in zip(base["cases"], candidate["cases"])]
    report = {"dataset_version": data["version"], "dataset_sha256": hashlib.sha256(raw).hexdigest(),
              "variants": variants, "paired_comparison": comparisons}
    (args.out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"report": str(args.out / "report.json"),
                      "macro_recall": [x["macro_recall"] for x in variants]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
