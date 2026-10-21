# Agent work in CI and pull requests

## Start here

Read the retained task, verification, and review lessons before this topic. **CI**, or continuous integration, runs configured checks when changes are proposed or integrated. A **pull request** presents a change for review. You can understand this lesson without a GitHub account or hosted runner. Use the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md) for a fictional walkthrough; do not upload your workplace secrets.

## The idea in plain language

Local success and CI success are different observations. They may use different operating systems, dependency versions, environment variables, and files. A green run also belongs to a particular commit, the identified source snapshot. If the branch changes afterward, the earlier green result does not automatically verify the new code.

An agent can propose code or help diagnose a failed job, but CI executes repository-controlled instructions. Those instructions may themselves be changed by a pull request. **Untrusted input** includes proposed code, issue text, branch names, and pull-request titles. **Privilege** means the ability to read sensitive data or perform actions such as publishing a release. Mixing untrusted changes with privileged credentials creates a boundary that needs deliberate design.

The goal is useful automation with limited authority. Read-only checks of a proposed patch often need less access than publishing artifacts or deploying. Separate those responsibilities, review the code that receives credentials, and use the platform's documented permissions. A passing test job does not certify that a workflow handles secrets safely.

## A small example

Signal Desk has a fictional pull request at commit A. Its unit tests pass. An assistant then adds a new dependency and pushes commit B. Reporting “CI passed” based on A is stale evidence. The reviewer needs the checks for B or an explicit statement that B remains unverified.

Now imagine the pull request also edits the workflow to execute a script supplied by the change with a deployment credential. That is a different review concern from whether the unit tests are green. The assistant should recognize both the code's functional behavior and the automation's authority boundary.

## Try it with Codex or Claude Code

```text
Explain this fictional pull-request situation without using GitHub or editing
files. Commit A passed CI. Commit B changed a dependency and a workflow script.
The workflow proposes running pull-request code with a deployment credential.
Explain which evidence is stale, which new checks are needed, and why the
credential boundary needs separate review. Define commit, job, runner and secret.
Show a concise truthful status report that does not claim B passed or deployed.
Do not provide real credentials or trigger a pipeline.
```

When working on a real repository later, inspect its existing workflow and policies first. Do not introduce a new privileged automation simply because an assistant can generate the YAML configuration.

## What you should see

The assistant should identify the exact source revision under discussion and separate proposed, executed, passed, and published states. It should recommend minimal permissions for each job without claiming that a prompt enforces them. An accurate handoff might say that local checks passed while the corresponding remote run is still pending. That limitation is useful information, not a reason to invent a green status.

## If it goes wrong

If the assistant says “works on my machine,” ask which dependency and runtime differences CI could expose. If it suggests printing environment variables to debug authentication, require redacted names and categories rather than values. If it proposes using a privileged pull-request trigger to bypass a permission failure, inspect the platform's security guidance first. A permission restriction may be protecting the intended boundary.

## Go deeper

Read [GitHub's Secure use reference](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions), especially Writing workflows and the risks of untrusted code checkout. Stop before third-party action selection. Public reading needs no account; actual Actions execution may consume account allowances. The retained [review and operations lab](../../labs/15-review-and-operations.md) offers synthetic delivery practice.

## Optional practice

Ask your tutor for one fictional run history containing two commits. Decide which claim the newest verified evidence supports before seeing feedback. You need not create a real pull request to learn evidence freshness.
