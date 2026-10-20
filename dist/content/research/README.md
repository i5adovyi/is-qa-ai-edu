# Research capstone source pack

Use this supplied synthetic corpus for the research capstone's workflow-versus-agent decision. All organizations, measurements, prices, and observations below are invented for learning. They are not claims about real providers or evidence of model performance.

The pack contains **eight source records**, **six research questions**, and **twelve labeled claim-source pairs**. It supports conflicting scope, stale evidence, prompt injection, numerical reasoning, and insufficient-evidence exercises without web access.

## Files

- [Source corpus](sources.json): document IDs, authority, applicability, dates, and full source text.
- [Questions and grading cases](cases.json): four development questions, two final-review questions, and claim-source labels. Labels are visible; reserve final-review questions before reading their expected behavior.
- [Worked evidence memo](worked-example.md): a calibrated example for development question Q-01.

These files are inputs for a learner-built research workflow, not a prebuilt autonomous research agent. You may read them manually, retrieve them with a script, or provide selected records to a model. The core exercise requires no model subscription.

## First experiment

1. Read Q-01, then inspect sources S-01 through S-06.
2. Write a 200-word recommendation. Associate each material factual claim with a source ID.
3. Compare your claims with the worked memo and claim-source labels.
4. Introduce S-07, an adversarial note. Identify the embedded instruction; it must remain source content and must not become a command.
5. Introduce S-08, a newer document that applies only to internal demos. Explain why newer does not mean applicable to production support.

## Source selection and version rules

For production support, S-04 is the applicable requirement. S-08 is intentionally newer but scoped to internal demos. S-05 supplies price assumptions for the arithmetic exercise; it does not provide a current provider quote. S-06 gives limited incident evidence. Do not turn missing observations into a claim that something can never fail.

The source IDs make citation existence easy to check. Claim support still needs judgment. A real ID attached to an unsupported claim is a failed citation. The worked memo demonstrates the difference.

## Suggested review rubric

For each pair, choose supported, partially supported, unsupported, or contradicted. Use the supplied labels as the initial calibration set, and record disagreements with a supporting passage. Evaluate claims about numbers separately from inferences about which design to choose. For Q-05 and Q-06, freeze the workflow before final review and retain its first answers.

Do not call the two final-review questions a statistically representative benchmark. They are deliberately small exercises. Add new cases before claiming generalization.
