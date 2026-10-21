# Inspect what you install before giving it access

## Start here

Read trust boundaries, permissions, and secrets first. You should know what a skill or MCP server is from the dedicated tracks. This topic explains the review decisions around installation; it does not install anything. Use an ordinary assistant conversation and the [assistant quickstart](../../../docs/ASSISTANT-QUICKSTART.md).

Your goal is to recognize that an attractive package description is separate from the behavior of its files, dependencies, and updates.

## The idea in plain language

A **software supply chain** is the set of sources and components used to produce and run software. In an AI toolchain it can include packages, model files, datasets, skill instructions, helper scripts, MCP servers, and remotely served tool descriptions. A **dependency** is another component your chosen component relies on; a **transitive dependency** is one it brings indirectly.

**Provenance** is information about origin and history. A version or commit pin makes a chosen source more reproducible, but does not prove it is benign. A lock file records resolved dependency versions. A signature can help establish who produced an artifact under a trust scheme; it does not certify that the behavior is appropriate for your task.

Read installation instructions as untrusted instructions until reviewed. A skill can contain useful prose and also call a script with broad filesystem or network access. An MCP server runs code or exposes a remote service; connecting it is not equivalent to reading a document. Review what will run and under which identity.

## A small example

Signal Desk considers a fictional “CI Summary Helper.” Its README says it summarizes test failures. Its manifest requests read access to all repositories, and a helper script posts full logs to an external analysis endpoint. An update changes that endpoint and adds a new install-time command.

The relevant questions are concrete: which repositories are needed, what leaves the machine, who controls the endpoint, what command runs during installation, and how are updates reviewed? A popular repository name or a high star count does not answer them.

You can inspect the supplied metadata in an isolated directory without granting live credentials. Testing with synthetic logs and restricted access can then reveal behavior before connecting real data.

## Try it with Codex or Claude Code

```text
Review a fictional tool package; do not install or fetch anything.
Name: CI Summary Helper. Advertised purpose: summarize selected CI failures.
Declared access: read every repository. Script behavior: send complete
logs to an external endpoint. Update: new endpoint plus an install command.
Explain the concrete evidence I should inspect before installation:
source identity, exact revision, dependencies, scripts, data destinations,
requested permissions, and update behavior. Define unfamiliar terms.
Separate facts supplied here from unanswered questions. Suggest a safe
synthetic demonstration, but do not claim the package is malicious or safe.
```

Review whether the assistant identifies unknowns rather than inventing a clean audit. A package can be unsuitable because its legitimate design exceeds your permitted data flow, even without malicious intent.

## What you should see

You should see an inspection sequence that connects behavior to authority and data. It should distinguish reviewing a README, inspecting code, running a controlled demonstration, and observing a real host installation. Those are different forms of evidence.

A useful installation record names the exact revision and the relevant reviewed behavior. On upgrade, compare the changed files and dependencies, rerun relevant checks, and reconsider permissions. “Previously approved” applies to the reviewed version and scope, not every future update.

## If it goes wrong

If the assistant proposes executing a remote installation command immediately, ask it to show and explain the downloaded source first. If the package requires administrator access without explanation, identify the operation that allegedly needs it. If review stops at direct dependencies, inspect important transitive dependencies and installation hooks too.

If the source is unavailable, record that limitation and decide whether the remaining assurances fit the use case. Do not pretend a black-box demonstration proves absence of hidden behavior. Keep real secrets out of exploratory testing and avoid changing the academy's intentional student stubs.

## Go deeper

Read OWASP's [Supply Chain risk](https://genai.owasp.org/llmrisk/llm032025-supply-chain/), the introduction and Common Examples of Risks. Stop before mitigation strategies on your first pass. Public reading requires no account. The AI-specific scope extends beyond ordinary packages; this lesson's helper scenario is an original illustration.

When you choose practice, use the retained [skill installation practice](../../skill-practice/README.md) and follow its disposable-workspace instructions. Installation and host behavior must be reported separately; a package validator alone does not prove the host used the skill.

## Optional practice

Ask your tutor for one fictional package update with changed permissions or destinations. Identify what must be reviewed again before you would accept it. Try before asking for feedback; no download or real installation is necessary.
