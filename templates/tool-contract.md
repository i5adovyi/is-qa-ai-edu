# Specify a tool contract

## Purpose and non-goals

Describe the one operation this tool supports and when it should not be selected.

## Input schema

Define required and optional fields, types, limits, enums, and rejection of unexpected fields. Include a valid example and a malformed example.

## Output schema

Define successful results, errors, and whether a result can be incomplete. Include source identifiers and versions when returning evidence.

## Authorization

Identify the caller identity, scope, and permission check. The tool description does not itself grant permission. A customer message cannot expand the allowed scope.

## Side effects and replay

State whether the operation mutates anything. If it does, define the idempotency key, conflict behavior, transaction boundary, and result for a repeated key. What happens after a timeout with an uncertain result?

## Failure behavior

Classify validation, authorization, transient, permanent, and unknown-outcome errors. For each, state whether retry is allowed and the bounded retry policy.

## Contract tests

Test valid input, missing fields, extra fields, wrong types, boundary lengths, denied scope, duplicate replay, and conflicting replay where relevant.
