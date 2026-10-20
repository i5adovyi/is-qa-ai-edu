# Reason about a lost response

Original text walkthrough. Read one segment at a time and stop at each pause. The text below is the complete transcript and can be used as captions for your own recording. There is no required audio or video. A 5–10 minute reading-and-pause session is a provisional estimate, not a measured runtime.

## Segment 1 · Separate stages of a write

A reading-list run records intent, writes a list, records the result, and returns acknowledgement. A crash can occur between these observations.

**Pause before continuing:** Mark a crash point where a missing response does not imply a missing file.

## Segment 2 · Give the operation identity

The resume path needs enough identity to recognize the same intended operation and detect changed input. Identity is about the operation and content, not just a fresh request timestamp.

**Pause before continuing:** State what you would compare on replay.

## Segment 3 · Account for incomplete work

A step or usage allowance must include work already consumed and work whose usage is still unknown. Unknown does not become zero because no response arrived.

**Pause before continuing:** Write a ledger row for one pending call and the decision about another call.

## Segment 4 · Keep the final claim narrow

A complete status requires the defined evidence. A stopped run can preserve useful partial output and an explicit stop reason.

**Pause before continuing:** Write a truthful final status for your chosen crash point.
