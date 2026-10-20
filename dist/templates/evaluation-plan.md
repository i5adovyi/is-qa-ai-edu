# Design an evaluation before tuning

## Claim under test

Write a falsifiable claim about the system. “Better answers” is too vague. “More tickets receive a supported category without increasing unauthorized calls” can be tested.

## Case population and sampling

Describe the users and tasks the cases represent. Separate training, development, and holdout use. Explain any synthetic generation and its limitations.

## Labels and rubric

Define correct, partially correct, abstain, and fail. Specify whether a safety or authorization failure overrides other scores. Record disputed labels and adjudication.

## Baselines and variants

Use a simple baseline. Change one relevant component at a time. State model and prompt versions, retrieval corpus version, and harness configuration.

## Measurement

Report numerator and denominator, important subgroups, latency distribution, tool failures, and actual cost where available. Do not hide failures in an aggregate average.

## Grader validation

If using a model judge, compare with human-labeled cases, randomize ordering where relevant, test verbosity bias, and record disagreements. Keep the judge prompt versioned.

## Release decision

Predeclare thresholds and failure conditions. Define what triggers a rollback or human review. Reserve fresh cases for the final check after tuning.
