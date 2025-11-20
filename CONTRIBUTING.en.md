# Contributing Guide

Thank you for your interest in the project — I appreciate any reasonable contribution.

## How to contribute

### 1. Fork & setup

```bash
git clone https://github.com/YOUR_USERNAME/faceit-ai-bot.git
cd faceit-ai-bot
git checkout -b feature/my-change
```

### 2. What I expect

- Run the project locally (see README).
- Make small, focused changes (one feature or one bugfix per PR).
- If you change core logic, add or update tests when possible.

### 3. Code style

- **Python**: follow PEP 8, use type hints.
- **TypeScript/Next.js**: keep ESLint/Prettier happy (as configured in the repo).
- Avoid noisy refactors that only reformat large files without real changes.

### 4. Commits

- Keep commit messages short and clear: what exactly changed.

Examples:

```bash
git commit -m "fix prod auth and Dockerfile"
git commit -m "update extension page and docs"
git commit -m "add training sample export for demos"
```

You can use Conventional Commits if you like, but it's **not required**.

### 5. Pull Request

```bash
git push origin feature/my-change
```

Then open a Pull Request to `pat1one/faceit-ai-bot` on GitHub and briefly describe:

- what you changed;
- why it is useful for users or the project;
- add a screenshot/example if relevant.

## Bugs and feature requests

- Bugs: open an issue with clear reproduction steps and a short description.
- Enhancements: open an issue with the `enhancement` label and explain what problem it solves.

## License

By contributing, you agree that your code is distributed under the custom **source-available** license described in [LICENSE](LICENSE).

---

**[Russian version](CONTRIBUTING.md)**
