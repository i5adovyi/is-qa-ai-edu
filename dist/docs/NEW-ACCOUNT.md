# Open the academy in another Codex account

Keep three things separate: **GitHub holds the course source**, **your computer holds local learning records**, and **an OpenAI Site has its own owner and URL**. Changing the account used by Codex does not copy chats, connect GitHub automatically, or transfer a Site.

## 1. Open the project in Codex

1. Keep the existing project folder, or clone the private repository with a GitHub account that has permission:

   ```sh
   git clone https://github.com/i5adovyi/is-qa-ai-edu.git
   cd is-qa-ai-edu
   ```

2. Sign in to Codex with the new OpenAI account. Open the existing local project folder in the app. Select the folder containing `AGENTS.md`, `academy.py`, and `content/`. Opening a local folder does not upload it to a new Site.
3. If you use a GitHub connector, reconnect GitHub from the new account and grant access to this private repository. Git credentials on your computer and a connector's repository permissions are separate.
4. Start a new chat in that project and use this handoff:

   > Read AGENTS.md and docs/CONTINUE-LEARNING.md. Tutor me using this academy, one exercise at a time. Ask for my latest attempt or progress export before deciding where I am. Do not show answers or incident debriefs before I try. Start from the next incomplete step and check my work against its criteria.

The repository instructions help a new tutor understand the project. They cannot restore an old conversation. Your attempts, notes, and feedback are preserved separately through the local database or a progress export. See [local data](LOCAL-DATA.md).

Codex availability and Sites access depend on the destination account. The local portal works without either service. See the official [Codex quickstart](https://learn.chatgpt.com/docs/quickstart) and [project instructions guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## 2. Continue locally with durable progress

From the project folder:

```sh
python3 academy.py local
```

The launcher opens the portal and saves local progress in `.academy-data/progress.sqlite3`. Reopening this same project uses the same database, including after signing in to another OpenAI account, changing browsers, or changing the server port. Keep the project folder and its ignored data folder; a new Git clone starts with no personal data.

If you previously learned in a hosted portal or an older browser-only local version, export its progress first. Import that JSON into the local portal and confirm a saved attempt and note. The local interface reports whether records were saved to the database.

Before moving computers, make a private database backup:

```sh
python3 academy.py backup --output ../academy-progress-backup.sqlite3
```

The output must not already exist. Keep it outside Git and hosted assets. [LOCAL-DATA.md](LOCAL-DATA.md) explains separate profiles, recovery, and moving the backup.

## 3. Prepare a new Site owned by the new account

The original clone contains the **original Site's identity** in `.openai/hosting.json`. Do not publish that identity as if it belonged to the new account. Make a separate publication copy:

```sh
python3 scripts/prepare_new_site.py --destination ../academy-new-account
```

Run this from the editable source project. Choose a destination that does not exist, outside the original project, whose parent directory already exists. In a portable download, first extract `dist/academy-source.zip` and run the command from that editable source folder.

The command copies the distributed course sources, builds a fresh `dist/`, sets `academy.json`'s `hostedUrl` to `null`, and writes `.openai/hosting.json` with only the static directory. It excludes the previous project ID, Git history, credentials in excluded locations, symlinks, runtime files, and learner databases/exports in their supported locations. It does not modify the original project, create a remote repository, or publish anything. Keep private files in the documented data/work locations; do not place secrets inside course lesson source.

The new folder is immediately usable locally:

```sh
cd ../academy-new-account
python3 academy.py local
```

It starts with an empty local learning profile. Import a progress JSON if you want to continue there. `python3 academy.py hosted` intentionally reports that no Site is configured until a new one has actually been published.

## 4. Create and publish from the target account

While signed in to the **target account**, open the prepared `academy-new-account` folder in Codex. With Sites available, ask:

> Create a NEW private OpenAI Site from this prepared academy folder under my currently signed-in account. Do not reuse the original academy's Site identity. Use the Sites workflow to register this folder and publish its `dist/` directory. Save the actual new project identity in `.openai/hosting.json` and actual resulting URL in `academy.json` as `hostedUrl`; rebuild after updating that URL, then publish the matching source and build. Preserve the repository URL. Keep learner databases, backups, and exports out of the upload. Verify the private access policy and return the new URL.

This step requires the supported Sites integration and the target account's access. There is no repository command that can create an authenticated Site in an arbitrary OpenAI account. Registration and publication must actually succeed before the new link is treated as ready. See the official [Sites guide](https://learn.chatgpt.com/docs/sites?surface=app).

Open the resulting URL while signed in as that account and import your progress JSON. The new Site uses browser storage, not your computer's SQLite database. Import/export is the supported bridge.

## Keep the two publication identities distinct

Continue course edits in the original private GitHub clone, or deliberately create a separate branch/repository for the new publication copy. The preparation command does not initialize or change a GitHub remote. The Sites integration manages its own source checkout for publication; do not replace its remote with a guessed URL.

To bring later course updates into the new Site, ask Codex to merge the desired GitHub changes while preserving that copy's new `.openai/hosting.json` and `academy.json` hosted URL, test, rebuild, and publish to **its** existing Site. Review the diff first. Never overwrite one account's hosting identity with the other's as a way to synchronize content.

[Run anywhere](RUN-ANYWHERE.md) · [Local data](LOCAL-DATA.md) · [Account migration checklist](ACCOUNT-MIGRATION.md)
