# Use AI in everyday testing work

AI assistance is most useful when you can review a small result against a clear expectation. Begin with explaining a failure, suggesting missing cases, or drafting one test. A whole test suite generated in one request is harder to inspect and can repeat the same mistaken assumption many times.

## Start with behavior, then code

Imagine a discount applies only to customers with an active subscription. An assistant sees an implementation that checks whether a subscription record exists. If it derives the expected result from that implementation, it may generate a passing test for an expired subscription. The test is consistent with the code and inconsistent with the requirement.

Provide the behavior separately from the implementation. Ask for candidate cases first when the behavior is ambiguous. Then supply a nearby test showing the actual framework, fixtures, naming, and cleanup conventions. You remain responsible for deciding whether each case tests an important behavior.

## Review the generated test as you would a colleague's change

An assertion should fail for a meaningful defect. Check whether it verifies an observable result or merely repeats the setup. A mocked dependency can make an impossible integration look correct. Broad exception handling, retries, or longer waits can conceal a failure. Assertions removed to make a test pass are a changed contract, not evidence of a fix.

Execution matters too. A claimed successful test run could have selected zero tests, used the wrong environment, or skipped the failing case. Read the command, the test count, and the relevant output. CI configuration, permissions, and data setup remain ordinary software engineering problems even when AI writes the change.

## Choose one assistant you can already access

Copilot, Codex, Claude Code, and other coding assistants differ in their interfaces, context selection, and permissions. You do not need to complete a course for each one. Learn the shared workflow: inspect the task, supply the relevant code and requirements, review a small change, run the relevant checks, and inspect what changed.

The selected GitHub tutorial below uses Copilot and Python. Read it as a concrete illustration if you use another assistant. Installing Copilot is optional. Product-specific buttons and commands are not the learning objective.

## Where SDET judgment adds value

AI can make it inexpensive to generate many tests. Your job is to decide which failures matter, whether the oracle is trustworthy, and whether maintenance cost is justified. Coverage percentages and a green run are useful signals with limits; neither proves the product meets its requirements.

Next, the direction changes: instead of using AI to test ordinary software, you will learn to test an AI feature itself.
