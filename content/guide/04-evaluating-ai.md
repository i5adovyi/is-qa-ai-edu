# Test software whose answers can vary

Consider a support assistant that summarizes a defect report. Two correct summaries may use different words. An exact string comparison is too strict, while accepting anything that sounds good is too weak. You need to define what makes the result useful for the actual task.

An **evaluation**, often shortened to **eval**, is a repeatable way to assess behavior on selected cases. It combines inputs, expectations, a scoring method, and a record of the system configuration. This should feel close to testing, but some expectations require a rubric and judgment rather than one literal output.

## Separate the things you can check

For a defect summary, deterministic checks can validate required fields, valid identifiers, output length, and whether cited records exist. A human can assess whether the summary preserves the important facts and avoids inventing a cause. An automated model grader may help scale that judgment, but it can also be inconsistent or wrong. Compare its decisions with human-reviewed examples before trusting its score.

A system might pass formatting checks and hallucinate a reproduction step. It might provide a correct summary and expose private information. Keep quality, safety, cost, and latency visible separately rather than hiding everything in one average.

## Choose cases that resemble your risks

Start from realistic tasks and known failures, using synthetic or approved data. Include clear requests, ambiguous requests, missing evidence, and cases where the correct response is to ask for clarification or decline an unsupported conclusion. Keep some cases separate from those used to tune the prompt. Otherwise you may optimize for the examples you keep seeing.

If an output can vary, one successful run is weak evidence of reliability. Repeated runs can reveal variability. Compare versions on the same cases and configuration, inspect changed failures, and choose an acceptable threshold based on the consequence of an error. A low-risk wording change and a wrong financial action should not share the same release rule.

## Fit evaluations into familiar engineering work

Keep fast deterministic checks in the ordinary test pipeline. Run model-dependent checks where their cost, latency, and credentials can be managed. Record prompt, model, tool, and dataset versions so a regression can be investigated. A provider change can alter behavior even if your application code does not change.

An evaluation suite samples behavior; it does not prove universal correctness. Production monitoring and new failure cases still matter. This is a direct extension of SDET work: better oracles, representative cases, and decisions supported by evidence.

Next, learn how an AI application obtains the documents it uses to answer a question. That introduces a separate source of failures: retrieval.
