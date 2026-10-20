# Work effectively with an AI coding assistant

This playbook turns a vague request into reviewable engineering work. Use it with your current assistant and consult the linked official product documentation in the resource library for exact interfaces. The operational habits transfer across products; file discovery, permissions, model names, and command syntax may not.

## Before starting

Choose a small outcome and a disposable practice directory. State the acceptance check before asking for code. Include the relevant files, the error output, and what you have already tried. Separate required behavior from optional improvements. Avoid asking for an entire application when you cannot yet explain one end-to-end user journey.

A useful opening request is: “The synthetic ticket router misclassifies a billing ticket when its text contains the word login. Reproduce the problem, identify the responsible rule, make the smallest justified change, and run the relevant checks. Preserve the public output schema. Report what changed and what remains untested.”

That request names a trigger, a process, a boundary, and evidence. It leaves room for the assistant to inspect the implementation without requiring it to obey a guessed diagnosis.

## Establish working context

Ask the assistant to read the repository's instructions and identify the commands for running it. Provide the task's input and output contract. Include only references needed for the next decision. If the task spans sessions, write a short handoff with the current state, completed checks, unresolved questions, and next action.

Do not confuse more text with more clarity. A huge conversation can contain conflicting decisions, stale outputs, and abandoned plans. Keep current decisions in a concise artifact and preserve detailed evidence in files that can be retrieved.

## During implementation

Request a checkpoint after a meaningful result: a reproduction, a working slice, or a completed test. Inspect the actual diff. If the assistant changes unrelated files, ask which acceptance criterion requires that change. If it claims a test passed, inspect the command and result. If the environment prevented a check, record that limitation and choose another check where useful.

When you give feedback, refer to observable behavior. “The error message omits the ticket ID” is actionable. “Make it smarter” is not. When the assistant is stuck, reduce the task, give a smaller failing input, or ask it to distinguish competing explanations with an experiment.

## At the permission boundary

Decide separately what can be read, what can be changed, and which actions have external effects. A model's proposed tool call is not an authorization record. Use the application's actual permissions and sandbox settings, and keep practice data synthetic. For a customer-facing action, review the proposed content and destination before enabling execution.

The academy's reference tools operate on local synthetic state. They illustrate a dispatcher boundary but do not constrain arbitrary Python code at the operating-system level.

## Before accepting the result

Run the targeted check and one relevant failure path. Verify the patch matches the requested scope. Read the final report for unsupported claims such as “fully secure” or “all edge cases covered.” Ask for the strongest remaining uncertainty. Save the result in an experiment log or version-control commit once you understand it.

A useful handoff has five parts: outcome, changed artifacts, checks and actual results, known limitations, and next action. It should let another person continue without recovering the entire chat.

## When to delegate

Delegate when subtasks have clear boundaries and integration contracts. Good examples include independent source research, test design on a fixed interface, or reviewing a completed patch. Poor examples include several workers editing the same small module without coordination. Start with one worker, measure the bottleneck, then test whether delegation improves it.

Use `templates/delegation-brief.md` to state ownership. The integrator remains responsible for reconciling assumptions and checking the combined result. Two agents agreeing does not establish correctness when both used the same faulty premise.

## A weekly improvement experiment

Choose one recurring task. Run it with your current process and record effort, defects, and rework. Change one part of the context, tool contract, skill, or review loop. Compare the result on new cases. Keep the change only if the evidence supports it. This is how you develop a personal workflow rather than accumulate untested prompting advice.
