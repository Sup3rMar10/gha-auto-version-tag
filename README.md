# gha-auto-version-tag

On every push to `main`, work out the next **semantic version** from [conventional commit](https://www.conventionalcommits.org/) messages, then tag it and create a GitHub Release with generated notes. No release is made when there is nothing release-worthy.

| Commits since the last tag | Next version |
|---|---|
| `type!:` or `BREAKING CHANGE` | major |
| `feat` | minor |
| `fix`, `perf` | patch |
| only `docs`, `chore`, `ci`, plain text | no release |

## What ran (2026-10-16)

| Commit pushed | Result |
|---|---|
| (initial commit, no tags yet) | no release |
| `feat: add greeting` | **v0.1.0** |
| `fix: punctuation in greeting` | **v0.1.1** |
| `docs: add notes` | **no tag** ("no feat/fix/breaking commits") |
| `feat!: rename greeting text` | **v1.0.0** |

The version logic has 7 unit tests, run in CI before it is used.

## The gotcha this repo demonstrates

A tag pushed with the automatic `GITHUB_TOKEN` **does not start workflows that listen for tag pushes** (GitHub does this to prevent loops). `tag-listener.yml` listens for `push: tags`, and across all three releases it was started **only by `workflow_dispatch`** (3 runs, 0 from a push event). The release job therefore starts it explicitly with `gh workflow run`. The alternatives are a personal access token or GitHub App token for the push, or doing the follow-up work in the same workflow.

## Decisions

- **`concurrency` without cancel**, so two quick pushes cannot race for the same version.
- **`fetch-depth: 0`**: tags and history are needed to compute the range.
- **Tag name through `env:`**, annotated tag, `--verify-tag` on the release.
- **Permissions:** `contents: write` and `actions: write` on the one job only. Credentials are persisted on purpose (it pushes a tag), which zizmor reports as `artipacked`.

## Honest limits

- The commit-message parser is simple: it does not handle reverts, pre-releases, monorepos or squash-merge titles specially. With squash merges, the **PR title** becomes the commit message, so enforce titles (see `gha-pr-automation`).
- A repository with tag protection rules or required PRs for tags would block this bot.
- No changelog file in the repo; notes come from GitHub's generator.

MIT licensed.
