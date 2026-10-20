# Keep learning after changing OpenAI accounts

Your course files and Python labs do not require this OpenAI account. Your private GitHub repository is controlled by GitHub access. The hosted Sites portal has a separate OpenAI access policy, and browser progress is stored separately from both.

## Before signing out

1. Open the portal's progress page and **Export progress**. Save the JSON file somewhere you control. It contains attempts, feedback, drafts, notes, recall history, and route preferences. Keep it private; do not commit it to the course repository.
2. Download the source ZIP and PDF, or keep your clone of [the private repository](https://github.com/i5adovyi/is-qa-ai-edu). The release also provides a portable portal bundle containing the already-built website.
3. Keep the [new tutor handoff](CONTINUE-LEARNING.md). It preserves how you want to learn, but is not a copy of the conversation or your browser records.
4. If you need the hosted portal with the new account, arrange access for that exact account email before signing out. An invitation must be accepted and verified while signed in as the new account. Access does not transfer ownership, subscription benefits, chat history, or connected-app credentials.

Do not rely on the old portal URL alone as your backup. An owner-only portal will not automatically admit a different account.

## Use the course locally with either account

From a Git clone or extracted source ZIP:

```sh
python3 scripts/build_portal.py
python3 scripts/serve_portal.py
```

On Windows, use `py -3` instead of `python3` if that is how Python is installed. Leave the server terminal open and visit the printed URL. Stop it with Ctrl+C.

The server listens only on your computer at `http://127.0.0.1:8765`. It does not sign in to OpenAI or publish a website. Use the same address and port each time so the browser can find its saved progress. If that port is busy, `--port 8766` uses another origin; import your progress backup there.

For the ready-built portable bundle, extract it and run:

```sh
python3 serve.py
```

It includes `dist/` and needs no build step. Reading lessons, hints, walkthroughs, and existing notes is local. External courses/videos need the internet. Optional live model and host labs still require an accessible model and their documented dependencies.

On the local portal, open Progress and import the JSON you exported. Check one saved attempt and one note before discarding any backup. Imports preserve conflicting versions rather than silently overwriting them.

## Use GitHub from the new OpenAI account

Sign in to GitHub with the account that can read the private repository. If using a GitHub connector from the new OpenAI account, connect it again and grant that repository explicitly. A working local Git clone and GitHub permission do not automatically configure the new OpenAI connector.

You can also open the local project directory in Codex and paste [the handoff](CONTINUE-LEARNING.md). Local files remain on disk when an OpenAI account changes. Back them up independently of any application login.

## Hosted access after the change

The original account remains the Site owner unless a supported ownership transfer is actually completed. Viewer access lets the next account use the portal, but is not a promise that it can administer or republish that Site.

If the original account becomes unavailable, use the local/GitHub copy. A new Site can be published from the source under the new account if that account has Sites access. It will have its own identity and URL. Preserve the old hosting identity until deliberately preparing a new Site; do not overwrite it as a shortcut.

Browser data is tied to its origin and browser profile, not automatically to your OpenAI account. Signing in elsewhere, opening a new Site URL, or clearing browser storage may give you an empty record until you import your backup.
