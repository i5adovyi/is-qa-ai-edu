# Starter cases before independent authoring

These small packs reduce the amount of invention needed for your first experiment. They are synthetic, authored teaching material. They are not captured customer data, measured model responses, or untouched final evaluation sets.

Use a pack in three passes:

1. **Attempt:** inspect inputs and sources; write your own labels or predictions before opening a key.
2. **Compare:** explicitly open the separate key after your attempt. Record disagreement, including places where the rubric needs clarification. Preserve your original labels.
3. **Transfer:** complete the original lesson exercise with new learner-authored cases. Freeze your split and rubric before tuning. Do not report success on inspected starter examples as unseen performance.

| Lesson | Starter material | First small task | Independent work still required |
| --- | --- | --- | --- |
| 05 retrieval | [Eight notes and six queries](lesson-05-starter.json) | Label required evidence for one query, then rank the notes | Author the original eight-note/six-query corpus, including a new exception and unanswerable request |
| 16 datasets | [Twelve input cases](lesson-16-starter.json) | Label two different failure dimensions and one expected/forbidden outcome | Author twelve new cases and establish eight development/four final cases before tuning |
| 17 graders | [Ten draft candidates](lesson-17-starter.json) | Grade two drafts against the supplied evidence without consulting the key | Author your own ten drafts, preserve disagreement, and calculate rates with declared denominators |
| 21 teams | [Eight paired comparison inputs](lesson-21-starter.json) | Run one normal case and one conflicting-source case with each configuration | Author eight new cases and run the full paired comparison with all parent/worker effort |

Copy a pack to your own `work/` directory before modifying it. In a text editor, create a separate labels file keyed by the stable case ID. The runtime receives input/evidence only; evaluator labels should not be inserted into a model's context.

The lesson 16 pack deliberately has no claimed held-out split: you can read all its inputs during preparation. It includes normal, ambiguous, malicious-input, tool-failure, and stale/conflicting-source examples. For tool failures, source text is absent from the runtime evidence even though the key identifies the underlying policy. This distinction is part of the exercise.

The lesson 17 pack includes authored candidate text. Do not attribute its outputs to a real model. Borderline completeness cases are deliberately unresolved until you declare what the rubric requires.

## Optional keys · Open after your attempt

These files are explicit reference material. They are not included in the default tutor packet.

- [Lesson 05 relevance labels](keys/lesson-05-labels.json)
- [Lesson 16 behavior labels](keys/lesson-16-labels.json)
- [Lesson 17 reviewed verdicts and reasons](keys/lesson-17-labels.json)
- [Lesson 21 expected comparison behavior](keys/lesson-21-labels.json)

An equivalent supported answer can be valid even if it uses different words. A key is not permission to hide an ambiguous rule or overwrite an honest first attempt.
