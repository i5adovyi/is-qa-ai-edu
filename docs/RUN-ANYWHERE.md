# Run the academy on OpenAI Sites or your computer

The same course and interface support two modes. Choose the hosted portal for immediate access, or a local copy for learning without an OpenAI login.

| Mode | Start here | Requirements |
| --- | --- | --- |
| OpenAI Sites | [Open the private academy](https://signal-desk-ai-engineering-academy.igor-sadovyi87.chatgpt.site/) | Internet and an OpenAI account authorized for this Site |
| Local computer | `python3 academy.py local` | An extracted source/portable copy and Python 3.9+ |
| Editable source | [Private GitHub repository](https://github.com/i5adovyi/is-qa-ai-edu) | GitHub permission for cloning or pushing |

## Start locally

Either download **Run anywhere → Download portable academy** and extract the entire ZIP, or clone the private repository:

```sh
git clone https://github.com/i5adovyi/is-qa-ai-edu.git
cd is-qa-ai-edu
python3 academy.py local
```

In an extracted ZIP, open a terminal in the folder containing `academy.py`, `academy.json`, and `dist/` or `scripts/`. Run the same last command. On Windows, use `py -3 academy.py local` if that is how Python is installed.

The launcher builds the site automatically when editable sources are present. The portable bundle uses its ready-built `dist/`. It opens your browser at [the local academy](http://127.0.0.1:8765/). Keep the terminal open and press **Ctrl+C** to stop. No packages, API key, OpenAI login or model subscription are needed for the local course. External resources and optional live-model exercises retain their own requirements.

`127.0.0.1` is your computer's loopback address: the site is reachable only on that computer. Use the printed address consistently; `localhost` and `127.0.0.1` are different browser origins even when they reach the same server.

Useful options:

```sh
python3 academy.py local --port 8766
python3 academy.py local --no-browser
python3 academy.py local --no-build
```

The first changes a busy port, the second prints the URL without opening a browser, and the third serves existing build files. After editing source, launch normally again to rebuild. An already-running server needs a separate `python3 scripts/build_portal.py` followed by a browser reload.

Existing commands still work: `python3 scripts/serve.py`, `python3 scripts/serve_portal.py`, and `python3 serve.py` in the portable bundle. These serve an existing build without opening a browser. Do not run two servers on the same port or open `index.html` directly from disk.

## Open the hosted version

Use the hosted link above, or run:

```sh
python3 academy.py hosted
```

This opens the existing private OpenAI Site. It does not run a local server, upload files, or grant access. Use `--no-browser` to print its URL only. The Site's existing owner and authorized next account retain access; the local version remains independent of that login.

## Move between modes without losing work

1. In the version where you have been learning, click **Export my progress**.
2. Open the destination version and click **Import progress**.
3. Check one saved attempt and note before discarding any backup.

Progress is browser-local. The hosted site, local addresses, different ports, and browser profiles have separate storage. There is no automatic cloud synchronization. The Git repository and portable ZIP contain course material, not your notes or attempt history. See the [account migration guide](ACCOUNT-MIGRATION.md).

## Update GitHub and OpenAI Sites

GitHub stores the editable source and generated release assets. Pushing a commit does not automatically deploy OpenAI Sites. The two destinations have separate publication steps.

After editing source, rebuild with `python3 scripts/build_portal.py`, run the [maintenance checks](MAINTENANCE.md), review the diff, commit and push to the private repository. Keep personal records under the ignored `work/` directory.

For OpenAI hosting, open this project in Codex with the Sites plugin available and ask:

> Publish the academy from this repository to its existing OpenAI Site. Reuse the project ID in `.openai/hosting.json`, build `dist/`, and preserve the current private audience.

The Sites workflow pushes the exact source state, saves a matching deployment version, and publishes it. Updating that Site requires an owner/editor account; viewing permission alone does not grant publishing rights. No publication token belongs in this repository or the browser bundle.

The tracked `.openai/hosting.json` selects the existing Site and its static `dist/` directory. `academy.json` contains the public-facing hosted and GitHub URLs used by both launchers and the portal. Preserve the existing Site identity when updating. To create a separate Site under a different owner, use a separate copy and the supported new-Site workflow, then update that copy's URLs.

[Fresh-copy setup](SETUP.md) · [Maintenance](MAINTENANCE.md) · [Account migration](ACCOUNT-MIGRATION.md)
