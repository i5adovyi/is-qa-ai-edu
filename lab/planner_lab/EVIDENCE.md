# Instructor execution evidence — open after your attempt

Recorded 20 October 2026. Synthetic support data only. This is an implementation audit, not a learner submission or a model-quality benchmark.

## What was executed

| Gate | Observed result |
| --- | --- |
| Scripted planner + fixture lookup | Two proposals, one validated lookup, one local draft |
| Scripted planner + actual MCP | Same runtime succeeded over the pinned SDK and stdio server |
| Actual model proposals + actual MCP | Requested `gpt-6-astra` via authenticated Codex CLI; proposed lookup, received actual MCP observation, then proposed a validated draft |
| Actual assistant host + same MCP server | Host called the tool, repaired an invalid argument after a server error, retrieved evidence, and produced a supported draft |
| Responses API adapter | Fake-transport and HTTP failure tests passed; live API execution **pending**, because `OPENAI_API_KEY` was unavailable |
| Student implementation | Intentionally incomplete starter, with a typed failure; learner work remains required |

Core tests ran on Python **3.9.6**: 24 passed and one optional MCP test skipped. In the MCP environment, Python **3.12.14** with **mcp 1.30.0**, all **25** tests passed. Codex CLI version was **0.163.0-alpha.10.2**.

The test suite exercises observation feedback, strict proposal/argument contracts, actual MCP, repeated actions, premature completion, malformed output, refusal, retry limits, HTTP error classification, cancellation, deadlines, terminating a child process, version mismatch, context/attempt/decision limits, and output provenance. One test deliberately accepts a structurally valid but false claim to demonstrate the need for semantic review.

## Actual outer-runtime run

The [saved live evidence](live-evidence.json) records the seven runtime events and original artifact hashes:

1. Request with catalog and no retrieved evidence.
2. Model proposal to call `lookup_article` for `KB-EXPORT-2`.
3. Runtime-validated dispatch.
4. Actual MCP result with product version 2.4 and untrusted-evidence label.
5. Second model request containing that observation.
6. Model proposal to complete with a local draft.
7. Validation and completion.

The run finished in **12.803 seconds**, with two planner attempts, one tool execution, and no retries. Reported input usage was **11,253** and **11,337** tokens; reported output usage was **36** and **104**. Those counts include CLI-provided context and are not token counts for the course request alone. The recorded model identifier comes from the explicit CLI request; no immutable server revision was exposed. Dollar cost was unavailable.

Claim review: the draft recommends retrying with seven days or fewer, then supplying the job identifier for escalation. Both are supported by the retrieved article. It makes no claim that an outage was resolved. This is one task, not an estimate of general model reliability.

## Actual assistant-host run

The separate [host evidence](host-evidence.json) preserves a useful real failure and repair:

- The first call supplied `article_id`; the server rejected it because `record_id` is required.
- The host's next call supplied `record_id`, and the actual server returned the article.
- The host then produced a draft grounded in that result. Post-run validation through `lab.policy.validate_decision` passed.

This run took **16.466 seconds**. The host reported **41,872 input tokens**, including **27,264 cached input tokens**, and **249 output tokens**. The larger context and extra repair belong to this host-controlled run; they should not be merged into the outer-runtime run's measurements.

During setup, resolving the virtual environment's Python symlink lost its installed SDK; the helper now retains the venv entry point, with a regression test. A subsequent host run initialized MCP but failed discovery when the CLI's `apps` capability was disabled. The host helper now leaves discovery enabled. The proposal-only adapter still disables host tools because its outer runtime owns execution.

These earlier failed attempts are described here rather than silently counted as successful first attempts. No shared configuration was changed. Live failure injection uses fake transport; the audit did not manufacture real rate limits or refusals against a paid service.

## Limits of these observations

- A working host login does not prove separate Responses API access.
- API request-shape tests are offline contract tests, not a live API compatibility guarantee.
- A successful citation check is not semantic entailment. Human review remains a separate gate.
- Cancellation stops the local operation; it cannot establish remote processing or billing cancellation.
- The scripted and actual model runs are separate evidence categories.
- Windows commands are documented, but these executions ran on macOS.
