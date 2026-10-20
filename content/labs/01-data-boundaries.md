# Lab 01 — Keep useful context, remove sensitive values

**Outcome:** implement a small redaction contract and explain why prompt context, durable state, and telemetry have different data needs. Suggested time: 45–75 minutes.

## The problem

A ticket may contain a useful error code, an email address, and a pasted credential. Copying all of it into every prompt, checkpoint, and log spreads sensitive material. Deleting the whole ticket prevents useful work. Context engineering begins with deciding what belongs in each channel.

The reference trace stores argument names and hashes instead of raw bodies. Its checkpoint still contains synthetic ticket data so the run can resume. This distinction matters: a clean trace does not mean every artifact is redacted.

## Observe

Run a fresh reference demo:

```sh
python3 -m lab.cli demo --out .lab-runs/lab01-observe
python3 -m lab.cli trace .lab-runs/lab01-observe/trace.jsonl --json
```

Open the run's `store.json`, `checkpoint.json`, and `trace.jsonl`. Write a three-column table: artifact, required data, unnecessary data. Predict where a hypothetical pasted key would appear. Inspect the files to confirm your prediction.

Do not insert a real credential. Use the synthetic form `sk-demo-abc123` and email domains ending in `.test`.

## Build

Implement `redact_sensitive(text)` in `lab/student.py`.

The contract:

- Replace email addresses with `[EMAIL]`.
- Replace synthetic keys beginning `sk-demo-`, followed by letters, digits, underscores, or hyphens, with `[KEY]`.
- Preserve surrounding punctuation, error codes, ticket IDs, times, and other useful text.
- Calling the redactor twice must have the same result as calling it once.

Example:

```text
Input:  Contact ada@example.test; key sk-demo-abc123. Error 503 at 12:00.
Output: Contact [EMAIL]; key [KEY]. Error 503 at 12:00.
```

Your function is an isolated exercise; editing it does not silently alter the reference harness's logging policy.

## Completion gate

```sh
python3 -m lab.cli practice --lab 01
```

All four public checks must pass. Add two of your own examples: one with an email plus-address and one where punctuation immediately follows a key. Record both expected outputs before executing them.

## Make the reasoning visible

Explain what the redactor cannot reliably detect. A short regular expression does not recognize every email grammar, encoded secret, connection string, or unusual credential. It also cannot decide whether a person's name is necessary for a business task.

Then answer: if you hash a low-entropy value such as an email address, have you anonymized it? Explain why deterministic hashes can still permit guessing or correlation. The trace's hashes support comparison; they are not a general privacy guarantee.

## Stretch

Add a small fixture set of 12 strings: six values to remove and six facts to retain. Score both leakage rate and accidental deletion rate. Improve one while checking the other. Compare replacing an email with `[EMAIL]` versus a stable per-run pseudonym; explain what each enables and exposes.

Deliver a one-page data-flow note showing original ticket → redacted model context → operational trace → checkpoint. Mark which copies are retained and why.

[Hints](hints/01.md) · [Solution discussion](solutions/README.md#lab-01) · [Next lab](02-context-budgets.md)
