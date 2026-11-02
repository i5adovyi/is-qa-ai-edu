# Run the academy on OpenAI Sites or your computer

The same course and interface support two modes. Choose the hosted portal for immediate access, or a local copy for learning without an OpenAI login and saving your progress in a local SQLite database. You can also open the editable project in Codex under another account and publish a separate private Site from it.

| Mode | Start here | Requirements |
| --- | --- | --- |
| OpenAI Sites | [Open the private academy](https://signal-desk-ai-engineering-academy.igor-sadovyi87.chatgpt.site/) | Internet and an OpenAI account authorized for this Site |
| Local computer | `python3 academy.py local` | An extracted source/portable copy and Python 3.9+ |
| Editable source | [GitHub repository](https://github.com/i5adovyi/is-qa-ai-edu) | Git to clone; write permission to push |

## Start locally

Either download **Run anywhere → Download portable academy** and extract the entire ZIP, or clone the repository:

```sh
git clone https://github.com/i5adovyi/is-qa-ai-edu.git
cd is-qa-ai-edu
python3 academy.py local
```

In an extracted ZIP, open a terminal in the folder containing `academy.py`, `academy.json`, and `dist/` or `scripts/`. Run the same last command. On Windows, use `py -3 academy.py local` if that is how Python is installed.

The launcher builds the site automatically when editable sources are present. The portable bundle uses its ready-built `dist/`. It opens your browser at [the local academy](http://127.0.0.1:8765/). Keep the terminal open and press **Ctrl+C** to stop. No packages, API key, OpenAI login or model subscription are needed for the local course. External resources and optional live-model exercises retain their own requirements.

`127.0.0.1` is your computer's loopback address: the site is reachable only on that computer. The supported launcher saves records in this project's `.academy-data/progress.sqlite3`. The same data directory works across local ports and browser profiles; keep browser exports when transferring to a hosted Site.

Useful options:

```sh
python3 academy.py local --port 8766
python3 academy.py local --no-browser
python3 academy.py local --no-build
python3 academy.py local --data-dir ../my-academy-data
```

The first changes a busy port, the second prints the URL without opening a browser, the third serves existing build files, and the fourth selects a separate learning profile. After editing source, launch normally again to rebuild. An already-running server needs a separate `python3 scripts/build_portal.py` followed by a browser reload.

Existing commands still work: `python3 scripts/serve.py`, `python3 scripts/serve_portal.py`, and `python3 serve.py` in the portable bundle. These serve an existing build without opening a browser. Do not run two servers on the same port or open `index.html` directly from disk.

## Open the hosted version

Use the hosted link above, or run:

```sh
python3 academy.py hosted
```

This opens the private OpenAI Site configured in this copy's `academy.json`. It does not run a local server, upload files, or grant access. Use `--no-browser` to print its URL only. A newly prepared publication copy has no hosted URL until its Site is actually created. The local version remains independent of that login.

## Move between modes without losing work

1. In the version where you have been learning, click **Export my progress**.
2. Open the destination version and click **Import progress**.
3. Check one saved attempt and note before discarding any backup.

The supported local launcher saves progress in SQLite and reports save status. Hosted Sites use browser storage, separate for each Site URL and browser profile. There is no automatic cloud synchronization. The Git repository and portable ZIP contain course material, not your notes or attempt history. See [local data and backups](LOCAL-DATA.md) and the [account migration guide](ACCOUNT-MIGRATION.md).

To make a database backup independently of the browser:

```sh
python3 academy.py backup --output ../academy-progress-backup.sqlite3
```

Choose an output that does not exist. Keep it private and outside the course source.

## Open in Codex using another account

Keep or clone the GitHub repository, sign in to Codex with your new OpenAI account, and open the local project folder. Its `AGENTS.md` gives a new tutor the course's one-exercise-at-a-time rules. A local database or progress JSON carries learning records; old conversations do not transfer automatically.

For a Site owned by that account, prepare a separate copy:

```sh
python3 scripts/prepare_new_site.py --destination ../academy-new-account
```

Then open that prepared folder while signed in to the target account and ask the Sites integration to create a **new private Site**. Follow the exact [new-account handoff](NEW-ACCOUNT.md); it explains authentication, a fresh hosting identity, and keeping future updates separate.

## Update GitHub and OpenAI Sites

GitHub stores the editable source and generated release assets. Pushing a commit does not automatically deploy OpenAI Sites. The two destinations have separate publication steps.

After editing source, rebuild with `python3 scripts/build_portal.py`, run the [maintenance checks](MAINTENANCE.md) and review the diff before sharing changes. Keep personal records under the ignored `work/` directory.

For OpenAI hosting, open this project in Codex with the Sites plugin available and ask:

> Publish the academy from this repository to its existing OpenAI Site. Reuse the project ID in `.openai/hosting.json`, build `dist/`, and preserve the current private audience.

The Sites workflow pushes the exact source state, saves a matching deployment version, and publishes it. Updating that Site requires an owner/editor account; viewing permission alone does not grant publishing rights. No publication token belongs in this repository or the browser bundle.

The tracked `.openai/hosting.json` selects the existing Site and its static `dist/` directory. `academy.json` contains the public-facing hosted and GitHub URLs used by both launchers and the portal. Preserve the existing Site identity when updating. The new-account preparation command writes a fresh manifest without the original project ID, and a `null` hosted URL, in the separate copy only. Registration and publication then supply that copy's real identity and URL.

[Fresh-copy setup](SETUP.md) · [Maintenance](MAINTENANCE.md) · [New account](NEW-ACCOUNT.md) · [Local data](LOCAL-DATA.md)
