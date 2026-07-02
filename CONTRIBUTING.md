# Contributing to SecQDevOps

Thank you for your interest in contributing to the SecQDevOps project and QNODE! We welcome contributions from researchers, engineers, and the quantum computing community.

## Getting Started

### Fork & Branch
- Fork the repositories to your GitHub account.
- Create a new branch for your work using descriptive names:
  - `feat/description` for new features
  - `fix/description` for bug fixes
  - `docs/description` for documentation updates
  - `refactor/description` for refactoring

### Commit Messages
We follow [Conventional Commits](https://www.conventionalcommits.org/) for clear, semantic commit history:

```
type(scope): subject

Detailed explanation of the change (if needed).
```

Examples:
- `feat(gateway): add OpenQASM 3.0 circuit validation`
- `fix(reducer): resolve numerical divergence in contraction aggregation`
- `docs(readme): update installation instructions`

## Code Quality

Before opening a pull request, ensure your code passes all quality checks:

1. **Run the test suite and linters:**
   ```bash
   make check        # For Go and Rust projects
   npm run check     # For Node.js projects
   ```
   This typically runs:
   - Linting (format, style, and correctness)
   - Type checking
   - Unit and integration tests

2. **Maintain test coverage:**
   - Aim for >80% test coverage on new code.
   - Add tests for any new functions, endpoints, or behaviors.

3. **Code style:**
   - Each repository documents its linting and formatting tools in its README or CLAUDE.md.
   - Run formatters locally before committing.

## Pre-commit hooks

Every repository ships a `.pre-commit-config.yaml`. **Recommended — set up once per
machine** so every *future* `git clone` installs the hooks automatically:

```bash
pip install pre-commit
pre-commit init-templatedir ~/.config/git/template \
  --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
git config --global init.templateDir ~/.config/git/template
```

For a repo you have **already** cloned (the template only applies to new clones),
enable the hooks once with:

```bash
pre-commit install --install-hooks
```

What runs when:

- **on `git commit`** — fast formatters + hygiene (trailing whitespace, EOF, LF line
  endings, large files, private keys) + a `gitleaks` secret scan.
- **on the commit message** — the message is **auto-fixed, not rejected**: the mandatory
  [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) scope is set to
  the repo name and `Co-Authored-By` / AI-attribution trailers are stripped (single-author
  policy); `commitlint` then validates the result.
- **on `git push`** — the heavier checks: lint, type-check, and tests (the same
  Makefile/npm targets CI runs).

Hooks stay current on their own: a `git pull` that brings an updated
`.pre-commit-config.yaml` (new tool versions, hooks, or the `commit-msg` auto-fix script)
takes effect on your next commit — no re-install needed.

Run them by hand anytime:

```bash
pre-commit run --all-files                        # commit-stage hooks
pre-commit run --all-files --hook-stage pre-push  # heavy checks
```

### Committing when a hook auto-fixes files

pre-commit **aborts the first commit whenever a hook rewrites a file** (e.g. `ruff-format`
reformats your code) — by design, so you can review auto-fixes before they land. The fixes
are already applied to your working tree; just re-stage and commit again.

To make that automatic, add this one-time git alias and use `git cf` instead of `git commit`:

```bash
git config --global alias.cf '!f() { s="$(git diff --cached --name-only)"; git commit "$@" && return 0; [ -n "$s" ] && git add -- $s; git commit "$@"; }; f "$@"'
```

`git cf -m "feat(scope): …"` re-stages the files you had staged and retries **once**, so the
commit goes through when the fixers left nothing unfixable — and still blocks on real
problems (a `gitleaks` hit, a non-fixable check, …).

## Pull Request Process

1. **Use the PR template:** When opening a pull request, fill out the provided template with:
   - A clear description of your changes.
   - Related issue(s).
   - Type of change (feature, bug fix, refactor, documentation, etc.).
   - Testing and validation details.

2. **Link issues:** If your PR resolves an issue, include `Resolves #<issue-number>`.

3. **Review and feedback:** Expect constructive feedback. We may ask questions or request changes to maintain project quality and consistency.

4. **All checks must pass:** Ensure CI/CD pipelines, tests, and status checks are green before merge.

## Multi-Language Projects

This is a polyglot codebase spanning Go, Rust, Python, and TypeScript. Each language has its own toolchain and conventions:

- **Go:** `make` commands; see the repo's Makefile.
- **Rust:** `cargo` commands; see Cargo.toml.
- **Python:** Check the repo's Makefile or `pyproject.toml` for the test runner.
- **TypeScript/Node.js:** `npm` or `yarn` scripts; see package.json.

Always consult the target repository's documentation for specific commands.

## Reporting Issues

- Use the issue templates provided (Bug Report, Feature Request).
- Be specific: describe the expected behavior, actual behavior, and steps to reproduce.
- Include relevant environment details (OS, language version, etc.).

## Security

If you discover a security vulnerability, please do **not** open a public issue. Instead, report it privately to [secqdevops@hs-rm.de](mailto:secqdevops@hs-rm.de). See our [SECURITY.md](./SECURITY.md) for details.

## Questions?

Feel free to:
- Open a discussion in the repository.
- Check existing documentation in each repo's README.
- Review the architecture documentation in the main workspace.

Thank you for contributing to making quantum computing more secure and accessible!
