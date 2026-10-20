# Start from a fresh copy

Use the hosted portal for reading, quizzes, and notes. Run Python commands in a terminal on your computer, from the project directory. The portal does not execute Python or install a skill for you.

## 1. Get the files

Choose one route:

- **GitHub:** sign in with an account that has access to this private repository, then clone it. A “repository not found” message can mean your Git credentials do not have access.
- **Download:** in the portal, open **Field manuals → Download full project**, extract the ZIP, and open a terminal inside its `ai-engineering-academy` folder. This route needs no Git.

For GitHub, run:

```sh
git clone https://github.com/i5adovyi/is-qa-ai-edu.git
cd is-qa-ai-edu
```

The remaining commands assume this directory is your current directory. Check that it contains `README.md`, `lab/`, `content/`, and `scripts/`. Open a second terminal in the same directory when the guide requests one.

## 2. Check Python

```sh
python3 --version
```

The core course needs Python 3.9 or newer and its standard library. No `pip install`, API key, or model subscription is required for the core lab. The optional MCP lab uses a separate Python 3.12 environment; follow its own setup when you reach Lab 09.

On Windows PowerShell, try `py -3 --version`. If it works, replace `python3` with `py -3` in the core commands. Shell examples elsewhere use macOS/Linux syntax: PowerShell does not use `\` for line continuation. Put such commands on one line, and use the Windows virtual-environment executable shown in the MCP manual. The automated audit ran on macOS; Windows instructions are guidance, not a claim that this edition was executed on Windows.

If Python is missing or too old, install a supported version from the [official Python downloads](https://www.python.org/downloads/), reopen the terminal, and check its version again. If `No module named lab` appears, return to the project directory before retrying.

## 3. Run your first experiment

```sh
python3 -m lab.cli demo
python3 -m unittest discover -s tests
```

The demo should report a completed billing draft and print a fresh directory under `.lab-runs/`. Open that directory's `result.json` and `trace.jsonl`. These are synthetic local records; the demo does not send a customer reply.

The test suite should finish with `OK`. Before installing MCP dependencies, its optional MCP tests are explicitly skipped; this is expected. The tests check the provided implementation. Your deliberately unfinished `lab/student.py` functions have separate practice commands: an initial practice failure is an assignment, not a broken installation.

## 4. Open the local portal

```sh
python3 scripts/build_portal.py
python3 scripts/serve.py
```

Open [the local portal](http://127.0.0.1:8765). The server command stays running; this is normal. Keep that terminal open, and use a second terminal for exercises. Press **Ctrl+C** in the server terminal when finished. If port 8765 is occupied, use `python3 scripts/serve.py --port 8766` and open `http://127.0.0.1:8766`.

Rebuild after editing lesson or portal source, then reload the page. Do not open `portal/index.html` directly or edit generated files under `dist/`.

The hosted portal and each local port have separate browser progress. Use **Export my progress** before switching, then **Import progress** at the destination. The ZIP and Git repository do not contain your browser notes. Keep an exported backup.

## 5. Keep your evidence

```sh
python3 -c "from pathlib import Path
p = Path('work/experiments')
p.mkdir(parents=True, exist_ok=True)
with (p/'first-run.md').open('x') as f:
    f.write(Path('templates/experiment-log.md').read_text())"
```

Save your baseline, prompts, outputs, and experiment logs under `work/`; it is excluded from Git and the downloadable course. Preserve before/after evidence. Commands that refuse an existing run directory are protecting your earlier work: choose a new output name instead of deleting the record.

Now follow [your first 90 minutes](START-HERE.md#your-first-90-minutes), then [the practice map](PRACTICE-MAP.md).

## Optional tools and later setup

| Route | Additional requirement | When |
| --- | --- | --- |
| Core lessons, Python labs, portal | None beyond Python | Start here |
| Real MCP | Python 3.12, an isolated environment, internet for the pinned dependency download | Lab 09 |
| Skill discovery and behavior | Installed, authenticated Codex CLI or desktop app; available model access | Lab 10; structural installation checks remain offline |
| Model experiments | An assistant you can access; label actual output separately from mocks | Model bridge and model-dependent exercises |
| Portal maintenance tests | Node.js 22+ for `node --test`; optional Playwright/browser for browser tests | Maintainers, not a learner setup requirement |
| Rebuild the PDF | ReportLab; optional PDF inspection libraries and Poppler | Maintainers; the finished PDF is already included |
