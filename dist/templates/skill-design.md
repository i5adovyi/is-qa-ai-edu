# Design a reusable agent skill

Use this as a design worksheet before writing a product-specific SKILL.md. It is intentionally a reference template, not an automatically installed skill.

## When it should activate

Write a narrow purpose and three natural-language requests that should trigger the workflow. Add three similar requests that should not trigger it.

## Required inputs

List required context, resources, and tools. Define what to do when an input is missing.

## Procedure

Keep stable operational knowledge in the procedure. Put long references in supporting files. State what must be inspected, what can be changed, how to verify success, and how to report failure.

## Authority boundary

The skill can describe how to do authorized work; it cannot grant permission for an unrelated action. State any sensitive side effects and the actual permission mechanism.

## Evaluation

Test trigger precision, false activation, missing input, a normal task, a tool failure, and an adversarial source. Compare against performing the task without the skill.

## Portability

Record which product and version you tested. Read its current official documentation for file locations, discovery behavior, supported metadata, and execution permissions.
