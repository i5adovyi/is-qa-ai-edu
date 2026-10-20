# Lab 15 — Review an exact draft, release, and recover

Allow 90–150 minutes after lessons 14 and 22–23. Python 3.9+; no external accounts. This single-writer classroom queue persists synthetic local state. Its reviewer name is an audit label, not an authentication mechanism.

## Inspect before deciding

```sh
python3 -m lab.practicum.review_queue init --out work/review-queue
python3 -m lab.practicum.review_queue show --out work/review-queue
```

The output includes the draft, full source excerpt, active release, revision hash, review status, and event history. Read the draft against its evidence. Write your decision and a reason. Use the actual revision printed by `show` in the following commands; `REVISION_FROM_SHOW` is a placeholder, not a valid hash.

```sh
python3 -m lab.practicum.review_queue review --out work/review-queue --revision REVISION_FROM_SHOW --verdict changes_requested --comment "Describe the specific correction."
python3 -m lab.practicum.review_queue revise --out work/review-queue --body "Write your revised evidence-backed draft here."
python3 -m lab.practicum.review_queue show --out work/review-queue
```

You may also choose `rejected` or `approved`. A revision changes the artifact identity and invalidates the earlier review. Inspect the new draft and source again before approving its new hash.

```sh
python3 -m lab.practicum.review_queue review --out work/review-queue --revision NEW_REVISION_FROM_SHOW --verdict approved --comment "Explain the evidence supporting your review."
python3 -m lab.practicum.review_queue apply --out work/review-queue --revision NEW_REVISION_FROM_SHOW
```

The effect is a synthetic local status change. No message is sent. Repeating `apply` with the same approved revision must leave exactly one effect. The effect and terminal state are stored together through an atomic file replacement.

## Prove stale approval is rejected

Use a separate fresh queue. Approve its first revision, then edit the draft. Try applying the old hash. Expect exit **2**, a stale-approval error, and zero effects. The new revision also requires a new approval. Test rejection and correction requests before approval; neither may authorize application.

Close your terminal, open another, and run `show` against the same folder. Confirm the pending draft and event history survive process restart. Do not edit the store directly. The integrity check detects accidental draft changes, but hashes are not protection against a malicious local owner.

## Rehearse release and rollback

Start another fresh queue and leave its draft pending. A deliberately inconsistent release must fail before changing state:

```sh
python3 -m lab.practicum.review_queue release --out work/review-queue --version v2 --knowledge v2 --validator v1
```

Expect exit **2**. Then activate a consistent pair and roll back:

```sh
python3 -m lab.practicum.review_queue release --out work/review-queue --version v2 --knowledge v2 --validator v2
python3 -m lab.practicum.review_queue rollback --out work/review-queue --version v1
python3 -m lab.practicum.review_queue show --out work/review-queue
```

Confirm the draft remains available, the transition history identifies both versions, and an old approval has not silently revived. Release identifiers are immutable: changing the meaning of an existing version is an error. This is a coupled-version rehearsal, not a deployment to a customer service.

An automated example is available for comparison:

```sh
python3 -m lab.practicum.review_queue rehearse --out work/review-rehearsal
```

Its report is explicitly labeled synthetic automated review. It does not replace your own review decision.

## Run the release checks in a clean environment

The repository's `.github/workflows/academy.yml` runs core Python and portal tests, the content checker, and the scripted integration gates. It uploads reports even when a gate fails. Read the workflow before executing it. It has no live-model credentials and performs no publication.

On a clean local clone, use Python 3.9+ and Node.js 22+:

```sh
python3 -m unittest discover -s tests
node --test tests/test_portal.cjs
python3 scripts/check_content.py
python3 -m lab.practicum.workers --out work/ci-workers
python3 -m lab.practicum.retrieval --out work/ci-retrieval
python3 -m lab.practicum.review_queue rehearse --out work/ci-review
```

Core runs explicitly skip optional MCP tests without the separate SDK environment. A green core job does not establish MCP or model integration. Preserve the CI revision, job result, and report artifacts; an example workflow file alone is not an executed CI result.

**Gate:** a real learner review, a stale-approval rejection, one-effect replay across processes, preserved pending work, rejected mismatched release, rollback evidence, and clean-environment checks. Explain the single-writer assumption and what would be needed before supporting concurrent reviewers.

[Queue implementation](../../lab/practicum/review_queue.py) · [Incident template](../../templates/incident-review.md)

Workflow action inputs were checked against the official [checkout](https://github.com/actions/checkout), [Python setup](https://github.com/actions/setup-python), [Node setup](https://github.com/actions/setup-node), and [artifact upload](https://github.com/actions/upload-artifact) documentation on 20 October 2026. The workflow uses their documented v7 actions; update deliberately when platform requirements change.
