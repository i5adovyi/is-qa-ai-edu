# Follow one request through an AI system

## Start here

Start this track after understanding tools and a bounded agent workflow. You do not need a monitoring account, cloud project, or running service. The example below is a short synthetic trace you can read in Codex or Claude Code. The [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) explains how to open that conversation.

Your goal is to locate the first unsupported assumption or failing step. “The AI gave a bad answer” names a symptom; it does not yet explain where to investigate.

## The idea in plain language

**Observability** means having evidence that helps you understand a system's behavior. A **log** records an event. A **metric** summarizes measurements, such as a count or duration distribution. A **trace** follows one request through related operations. A **span** represents one operation within that trace, usually with timing, identity, and outcome.

For an AI workflow, useful operations include receiving the task, retrieving sources, calling a model, validating its proposal, calling a tool, and producing the response. Record actual boundaries and outcomes, not just the assistant's narrative about what it thinks happened.

Use a correlation or request ID to connect records from the same run. Also retain relevant configuration identities, such as the prompt revision and retrieval snapshot. Avoid full secrets and customer text when stable references and sanitized fields provide enough evidence. A trace should help investigation without becoming an uncontrolled copy of private data.

## A small example

Signal Desk produces this fictional sequence:

```text
request=demo-17 event=request_received prompt_revision=p4
request=demo-17 event=retrieval_completed source_ids=[] duration_ms=90
request=demo-17 event=model_completed output_claim="retention is 30 days"
request=demo-17 event=validation_completed allowed=true rule=format_only
request=demo-17 event=response_sent status=200
```

The request returned successfully at the HTTP layer: status 200. That says nothing about whether the answer was supported. Retrieval found no sources, and the validator checked only format. The trace suggests where to investigate, but does not establish why retrieval returned nothing. Possible causes include no matching documents, permission filtering, or an indexing problem.

This distinction matters: observed evidence identifies a gap; a root-cause claim needs additional evidence.

## Try it with Codex or Claude Code

```text
Read this synthetic trace; do not access real logs or run commands.
demo-17: request received, prompt revision p4.
demo-17: retrieval completed, source_ids=[], duration 90 ms.
demo-17: model claimed "retention is 30 days".
demo-17: validator allowed output using rule format_only.
demo-17: response sent with HTTP 200.
Explain logs, metrics, traces, and spans using this example.
Separate observations from hypotheses. Identify the next evidence needed
to distinguish no matching documents, access filtering, and index failure.
Explain why HTTP success does not prove answer quality. Invent no records.
```

Check each stated observation against the five lines. Ask the assistant to label any unsupported explanation as a hypothesis. It should not call the model “broken” merely because the answer is unsupported.

## What you should see

You should see a useful investigation order: confirm the intended source scope, inspect retrieval status and filtering, and determine whether a grounding check was expected before response. The explanation should distinguish missing evidence from an explicitly failed operation.

When comparing runs, preserve timing units and whether stages overlap. Adding the durations of parallel spans can exceed total elapsed time; that is not necessarily a bug. A missing end record might reflect a crash, sampling, or logging failure. It is not automatic evidence that the operation never happened.

## If it goes wrong

If every component reports “success,” ask what success means for each component. A model-call success may mean only that a response arrived. If a trace includes no source or configuration identity, you may be unable to reproduce the decision. Add the smallest useful metadata instead of dumping all content.

If a dashboard average looks healthy while users report delays, inspect distributions and affected slices. If logs disagree across services, verify request identity and clock assumptions. Keep the uncertainty explicit until additional evidence resolves it.

## Go deeper

Read OpenTelemetry's [Traces](https://opentelemetry.io/docs/concepts/signals/traces/), the opening request example and Spans definition. Stop before the detailed span attributes and SDK sections. Public conceptual reading requires no account. Instrumentation and telemetry export require separate setup and are not performed here.

Continue to the retained [service reliability lesson](../../how-to/22.md). The [traces and diagnosis lab](../../labs/07-traces-and-diagnosis.md) offers optional runnable practice with controlled examples.

## Optional practice

Ask your tutor for one new six-line trace with an ambiguous failure. State one observation, one hypothesis, and the next evidence you would obtain before asking for feedback. You do not need to build a dashboard or write an incident report.
