# Lab 03 — Give the model proposals, give the harness authority

**Outcome:** enforce a tool request's name, argument contract, and resource scope outside the policy. Suggested time: 60–90 minutes.

## The problem

A generated string saying “read ticket T-002” is a proposal. It becomes an authorized operation only after the application validates it. Good prompt wording can help the model choose a useful action; it cannot grant permission to cross account or ticket boundaries.

Signal Desk makes the boundary visible. `policy.py` decides. `tools.py` checks the allowlist, schema, ticket scope, approval grants, and budgets. The store only receives validated operations.

## Observe

```sh
python3 -m lab.cli schemas
python3 -m lab.cli demo --scenario invalid-tool --out .lab-runs/lab03-invalid
python3 -m lab.cli demo --scenario denied-tag --out .lab-runs/lab03-denied
python3 -m lab.cli demo --scenario approved-tag --out .lab-runs/lab03-approved
```

The invalid-tool and denied-tag commands intentionally fail. Compare their traces. Why does the denied-tag run have one draft even though its terminal status is `failed`? Why is that not a permission bypass?

The approved-tag scenario creates a synthetic ticket-specific grant to demonstrate authorization. It does not contact a user or represent a real application's approval UI.

## Build

Implement `tool_allowed(name, arguments, allowed_tools, ticket_id)`.

For this narrow exercise, return `True` only when:

- The name is exactly `read_ticket`.
- `read_ticket` appears in the externally supplied allowlist.
- Arguments are a dictionary with exactly one key: `ticket_id`.
- Its value is a string exactly equal to the authorized ticket ID.

Return `False` for every other input, including malformed arguments. Do not perform the read. This function is a pure policy check.

An allowlist that happens to contain `run_shell` must not make that unknown tool valid. A known name must also have a known contract.

## Completion gate

```sh
python3 -m lab.cli practice --lab 03
python3 -m unittest discover -s tests -p 'test_lab_contracts.py' -v
```

All six student checks and the baseline contract tests must pass. Add adversarial inputs for a numeric ticket ID and a missing key. Explain why accepting `**arguments` without checking extra fields can weaken a future tool implementation.

## Threat model in one page

Identify:

1. The protected resource: the ticket authorized for this run.
2. Untrusted input: ticket text and any generated tool proposal.
3. Application authority: tool registry, allowed names, scope, approval grants.
4. The failure you are preventing: a proposal becoming a cross-ticket read or unauthorized mutation.
5. What remains outside this toy boundary: host filesystem access by Python code, concurrency, malicious local checkpoint edits, provider transport, and real identity authentication.

Do not present the tool allowlist as an operating-system sandbox. They solve different problems.

## Stretch

Design a `save_draft` contract with maximum reply length, unique citations, ticket scope, and an idempotency requirement. Specify which checks belong at schema validation, authorization, evidence validation, and mutation execution. For each check, add one negative test that would fail if the check were removed.

[Hints](hints/03.md) · [Solution discussion](solutions/README.md#lab-03) · [Next lab](04-retries-and-budgets.md)

## Connect it to the complete harness

This lab teaches one component contract. After completing Labs 01–08, follow [Lab 11](11-complete-student-harness.md) to use this function in real runs with component evidence, crash recovery, and an integrated acceptance gate. The ordinary reference evaluation does not call this student helper.
