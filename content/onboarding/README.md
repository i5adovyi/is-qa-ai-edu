# Begin with one small result

You do not need to understand the entire architecture before starting. These three entry checks are independent. Complete the first two for the concept route. Add the third before the Python labs. Estimated time: 15–25 minutes for the first two, another 20–40 minutes for the terminal check. These are planning estimates, not observed learner timings.

## Entry check A · Read a tiny diagram

A box names a responsibility. An arrow names information passed between responsibilities. It does not automatically mean “the next thing in time.” One box can receive several kinds of information.

Here is an unrelated example: preparing a packing list for a hiking trip.

```text
[Trip form] -- destination and dates --> [Forecast lookup]
[Forecast lookup] -- forecast with date/source --> [Packing suggestion]
```

The form captures what the traveler entered. The lookup gets weather information. The suggestion uses that information. The diagram does not establish that the forecast is correct, that the traveler owns the equipment, or that a trip has been booked.

**Your check:** say what each box is responsible for and what crosses the second arrow. Then add a `Bag-weight check` box and one arrow of your own. Explain its label in one sentence. There is no single required drawing style.

**Pass:** responsibilities and data are distinguishable; your arrow label names information, not just “process.” If you are stuck, use the [diagram worksheet](../../templates/first-diagram.md) and the [short walkthrough](../walkthroughs/01-diagrams-and-outcomes.md).

## Entry check B · Separate a proposal, a tool result, and an outcome

Consider these events in the hiking example:

```text
1. An assistant writes: “I recommend a waterproof jacket.”
2. A lookup returns: {"forecast_date":"2026-10-21","rain_probability":0.7}
3. A person inspects the bag and records: “Jacket packed, checked at 18:10.”
```

Event 1 is a generated proposal. Event 2 is a tool's returned observation, with a limited meaning: it is a forecast, not proof that rain occurred. Event 3 is evidence for a specific physical outcome. None establishes that the whole trip is ready.

**Your check:** a recipe assistant says “I saved your shopping list,” but the file-writing tool returned `permission_denied`. Write what is known, what remains unverified, and the next check you would make. Do not use the hiking wording as your answer.

**Pass:** your completion claim is no broader than the observed result. You can distinguish helpful language from an effect that actually occurred.

## Entry check C · Use the terminal and inspect a failed check

This check uses only the Python standard library. Work from the academy repository root. It creates a disposable copy under `work/onboarding/`; it never changes the supplied fixture.

```sh
python3 content/onboarding/terminal_practice.py init
python3 content/onboarding/terminal_practice.py run
python3 content/onboarding/terminal_practice.py check
```

The final command is **supposed to fail at first**. Read the assertion, open the printed input and output paths, and identify the field involved. Edit only your `work/onboarding/request.json`, rerun `run`, then `check`. Do not edit the checker to make it pass.

**Deliverable:** the original failure, the changed JSON field, the regenerated output, and the passing check. Explain why editing the input alone did not update the old output file.

**Pass:** you can find the files, edit valid JSON, regenerate the result, and explain the failed assertion. Use the [terminal catch-up worksheet](terminal-worksheet.md) if any step is unfamiliar. Passing this check is preparation; it does not claim you can program independently.

## Choose your route

| Route | Begin now | Evidence still pending |
| --- | --- | --- |
| Concept | Entry checks A/B, lesson 01, paper artifacts and applied checks | Executed code, actual MCP, host behavior, and live model runs |
| Local engineering | All entry checks; core labs, actual MCP where its dependencies are installed | Live model behavior and actual assistant-host trials until performed |
| Live model | Local work plus an authenticated provider or assistant host, with your own spending limits | Any provider, model, failure, or host you did not actually test |

The routes share the same reasoning objectives. They do not confer the same execution evidence. Use “pending” for unavailable integration work and continue the useful work you can perform.

## Your first lesson, one checkpoint at a time

Open [lesson 01](../lessons/01-systems-before-agents.md#exercise-1--guided-map). Start with its first checkpoint only. Record your attempt in the portal exercise workspace or [attempt record](../../templates/exercise-attempt.md). Request one hint when you need it; no minimum struggle time is required.

At the end of preparation, record actual minutes, checkpoints completed, and where you requested help in [the pacing log](../../templates/pacing-log.md). Estimates become more useful through these observations. The course does not claim a beginner trial has already validated them.
