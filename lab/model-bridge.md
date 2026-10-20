# Model bridge: test a real model's saved answer

**Outcome:** compare a chat model's decision with the deterministic baseline, then replay its answer through Signal Desk's real output validator, tool permissions, budgets, storage, and evaluation. Allow 45–90 minutes. Requirements: Python 3.9+ and optionally any chat model you can access.

The bridge makes no network calls and needs no API key or provider SDK. You paste a synthetic task into your chosen model and save its answer yourself. This is a working experiment with one bounded model decision. It does not implement autonomous tool planning or a live provider transport. The seven earlier helper functions remain isolated micro-exercises; this bridge and lab 08 connect decisions to the working harness.

## 1. Export a request

From the repository root:

```sh
python3 -m lab.model_bridge export --case train-01 --out work/model-01
```

The command creates:

| File | Purpose |
|---|---|
| `prompt.md` | Paste-ready instructions, ticket, retrieved articles, decision contract |
| `request.json` | Inspectable structured copy of the request |
| `mock-response.json` | **Deterministic reference response; not AI model output** |
| `README.md` | Provenance and handling notes |

Use a fresh directory for each experiment. The exporter uses the same fixed classifier and approved knowledge selection as the reference harness. It does not export expected case labels or the evaluator's required/forbidden phrases into the prompt. Approved articles necessarily contain product facts the model needs.

Read `prompt.md` before pasting it. It contains fictional data only. Record your model's displayed name, provider, date, visible settings, and your exact prompt in an experiment log. Do not enter real customer data, account tokens, or credentials.

## 2. Obtain and save a response

Paste the full `prompt.md` into a fresh model conversation. Ask for the JSON object specified in the prompt. Save only that object as `work/model-01/response.json`, using your text editor. Do not save Markdown fences or explanatory paragraphs around the JSON.

If the model returns invalid JSON, preserve the original output separately and record the formatting failure. A repair or manual edit is a new intervention: record it and keep both versions. Do not quietly fix the model's citations, facts, or action before calling the result a first-attempt success.

No model access today? Skip the chat step and use `mock-response.json` in the next command. That verifies the engineering path offline; label its results **mock baseline**, never model results.

## 3. Replay through the harness

For your saved model response:

```sh
python3 -m lab.model_bridge run --case train-01 --response work/model-01/response.json --out .lab-runs/model-01
```

Offline smoke test using the explicitly labeled mock:

```sh
python3 -m lab.model_bridge run --case train-01 --response work/model-01/mock-response.json --out .lab-runs/model-01-mock
```

Keep the `--case` value the same as the exported request. The replay loads the original fixture and retrieves its evidence again. A copied response is only a proposal; `Runner` validates its exact schema and citation relevance before calling `save_draft`. Extra fields cannot grant tools or permissions.

Inspect `bridge-report.json`, `provenance.json`, `result.json`, `store.json`, and `trace.jsonl` in the output directory. The report shows all eight case acceptance checks, writes, drafts, tool calls, and harness usage. Exit `0` means the case acceptance checks passed; `1` means the response failed the gate; `2` means invalid input or command configuration.

Malformed JSON, duplicate fields, nonstandard numbers, invalid UTF-8, and files above 64 KiB are rejected before creating run artifacts. Parseable but invalid decisions produce a failed run and **zero draft/tag writes**; the run still creates local diagnostic artifacts. Ordinary read/retrieval observations occur before the decision validator, just as they do in the reference harness.

The provenance record hashes the response and identifies it as **user-supplied saved JSON**. It cannot verify model authorship or whether you edited the answer. The response file is read only and never overwritten. Valid responses appear in the checkpoint and draft store, while traces retain bounded metadata and hashes.

## 4. Make the boundary fail

Create copies of your saved JSON and run each into a fresh output directory:

1. Replace its citation with `KB-NOT-RETRIEVED`. Expect `unsupported_citation`, no draft, zero writes.
2. Add `"execute": "send this to a customer"`. Expect `invalid_decision`, no draft, zero writes.
3. Return a valid escalation for `train-01`. Expect status `escalated`, but case acceptance **FAIL**: this supported billing task should receive a grounded draft.
4. Add an unsupported guarantee to an otherwise well-formed reply. Inspect both the automated content checks and the source yourself. The validator proves schema/provenance, not that every claim is true.

Write down predictions before running. Preserve each failed report and explain which layer rejected the answer.

## 5. Run a controlled comparison

Export `train-01`, `train-03`, `train-05`, `train-09`, and `train-13` into separate directories. Before obtaining answers, record a comparison plan: baseline prompt versus one changed prompt, same model, same five cases, separate fresh conversations, and a rule for counting manual repairs. Run both conditions and preserve the ten response hashes and reports.

Record:

| Measure | Evidence |
|---|---|
| Case acceptance | Passed cases / attempted cases; keep parse failures in the denominator |
| Draft usefulness | Human review of whether the request was actually answered |
| Grounding | Label each factual claim supported, contradicted, or not established |
| Abstention | Correct escalation versus missed supported work |
| Operational effects | Drafts, writes, tool attempts, rejections from run artifacts |
| Model effort | First attempt versus repair; manually observed time if measured |

Five cases give you a debugging comparison, not a reliable benchmark. Repeated model sampling may change results. Virtual milliseconds and character counts are harness accounting, **not model latency, token usage, or cost**. Record provider usage only if the product actually exposes it; otherwise mark it unavailable.

Use training cases while iterating. A holdout export requires an explicit holdout case ID; freeze prompts and settings before that final check, and do not tune against its labels afterward.

## Deliverable

Submit an experiment note with the model/settings/date, exact prompt versions, saved response hashes, reports for successful and failed cases, one rejected mutation proposal, claim-level human review, and a conclusion supported by those observations. Distinguish measured facts from unknown provider details.

Next: [implement a provider adapter](provider-adapter-design.md), including fake-transport failures, deadlines, and cost accounting. The manual bridge establishes the decision boundary you will keep.
