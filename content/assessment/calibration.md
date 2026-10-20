# Calibrate judgment using a different problem

These are original, authored specimens. They are not real student submissions, captured model runs, or claims that commands were executed. Each set assesses one stated dimension. A strong paper design does not establish a passing implementation.

Before reading each annotation, assign a score from 0–4 using the [common rubric](../../docs/ASSESSMENT.md#common-scoring-rubric). Then compare the reasoning, not just the number. The scenarios deliberately differ from the assigned Signal Desk cases.

## Set A · Task definition for a recipe shopping list

**Task context:** a person provides a recipe and a pantry list. The system may prepare a local shopping list. It cannot buy groceries, claim current shop stock, or infer an unknown allergy is absent.

### Weak specimen

> Make the best shopping list. Be an expert chef and finish everything. If anything is missing, use your judgment.

**Annotation — task definition: 1/4.** There is a broad purpose, but “best” and “everything” supply no observable completion test. The instruction leaves purchasing authority, missing quantities, and dietary uncertainty ambiguous. A reviewer cannot decide what should happen if the recipe mentions “some nuts.”

**Smallest useful revision:** name input fields, output fields, and what happens when a quantity or allergy constraint is unknown.

### Adequate specimen

> Read recipe ingredients and the supplied pantry inventory. Return a local list of missing ingredients with quantities. Do not purchase anything. Ask for clarification if an ingredient amount is absent.

**Annotation — task definition: 2/4.** A normal case is reviewable and external authority is bounded. Unit conversion, inventory freshness, and dietary conflict remain unaddressed. The specification supports a happy-path example but does not yet define relevant difficult cases.

**Smallest useful revision:** provide a contrastive case where the same ingredient has incompatible units or a stated dietary restriction.

### Strong specimen

> Input: recipe text, dated pantry inventory, and explicit dietary restrictions. Output: `items`, `unresolved`, and `source_refs`; each item has name, quantity, unit, and recipe reference. Subtract inventory only where identity and units are compatible. Put absent amounts, unknown substitutions, and incompatible units in `unresolved`. A stated dietary conflict blocks a ready status. Save locally; do not purchase or assert shop availability. Done means every recipe ingredient appears as covered, needed, or unresolved. Check three cases: all quantities compatible; grams versus “one packet” without conversion; a nut ingredient with a stated nut allergy.

**Annotation — task definition: 4/4.** The contract is bounded, covers normal and decision-changing cases, preserves uncertainty, and defines accounting for every ingredient. It explains a deliberate limit: unknown conversions become review work. This score applies to the contract only; implementation and health-related suitability have not been validated.

## Set B · Context quality for a library recommendation

**Sources supplied:**

```text
CAT-1, recorded Monday: Branch North has one print copy of Book A.
CAT-2, recorded Tuesday: Branch South has two ebook licenses for Book A.
RULE-1: Recommendations may cite catalog observations but may not promise
availability at pickup. Print holds and ebook loans are different services.
Request: Find a print copy at Branch North for pickup on Friday.
```

### Weak specimen

> Book A is available, so your Friday pickup is guaranteed.

**Annotation — context quality: 1/4.** It erases source identity, date, branch, format, and the no-guarantee rule. It converts a catalog observation into a future promise. Mentioning the title is the only preserved useful fact.

### Adequate specimen

> CAT-1 lists one print copy at Branch North as of Monday. Check availability again before pickup.

**Annotation — context quality: 2/4.** The relevant source and its temporal limit are preserved. The packet does not record the request's Friday date, the explicit policy basis, or why the newer South ebook observation was excluded. A happy path is understandable, but a resuming reviewer lacks the selection reasoning.

### Strong specimen

> Goal: identify a possible Friday print pickup at North, without making a reservation. Applicable observation: CAT-1, Monday, one North print copy. Newer CAT-2 covers South ebooks and does not establish North print availability. RULE-1 permits recommendations but forbids guaranteeing pickup from a catalog observation. Unknown: current stock and future availability. Next action: query current North print stock; if absent, report the gap. Preserve CAT-1 as historical evidence, not a live stock claim.

**Annotation — context quality: 4/4.** Scope, provenance, freshness, exclusions, and the next observation are explicit. The packet is useful without hidden chat history and does not erase the more recent but inapplicable source.

## Set C · Evaluation reporting for a document extractor

**Authored example results:** four fixed synthetic pages, A–D. The task is to extract invoice ID and total without inventing missing values. Baseline passes A/B/C and fails D. Candidate passes A/B/D and fails C. Case C omits a total; candidate invents one. Case D uses an unusual but valid layout. These are supplied teaching observations, not an executed benchmark.

### Weak specimen

> The candidate is excellent. It solved the tricky page and is production ready.

**Annotation — evaluation: 1/4.** It omits the denominator, baseline, regression, synthetic provenance, and definition of success. “Production ready” is unsupported.

### Adequate specimen

> Baseline and candidate both passed 3/4 pages under the invoice-field rubric. The candidate improved D but regressed C. These four pages are synthetic.

**Annotation — evaluation: 2/4.** The comparison and discordant cases are visible. The report does not yet discuss the severity of invented totals, split exposure, or a next experiment.

### Strong specimen

> On the four supplied practice pages under rubric v1, both systems passed 3/4. A/B passed in both; D improved; C regressed because the candidate fabricated an absent total. Our predeclared missing-value gate rejects fabricated amounts, so this candidate is not releasable even though it handles one more layout. All pages were inspected during development; this is not held-out evidence. Preserve the C failure, revise missing-value handling, compare again on these development pages, then use a separately authored final set. The supplied observations illustrate reporting only; a runnable implementation, environment, and actual result files remain required.

**Annotation — reporting quality: 4/4; execution evidence: still absent.** It makes the comparison auditable, applies a severe-failure gate, preserves exposure history, and states its limits. Do not convert its excellent report structure into a 4/4 reproducibility score without an actual runnable package.

## Apply the calibration

Choose one of your own artifacts. Identify the closest specimen, cite one passage supporting your score, and make the smallest revision that would justify the next level. Ask a reviewer to disagree using the same criterion. Keep that disagreement; it can expose a vague rubric.
