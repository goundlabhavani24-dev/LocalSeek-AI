# Contributing Guidelines

Thank you for contributing to **LocalSeek AI**! To maintain code quality and collaborate effectively during the hackathon, please follow these guidelines.

## Development Workflow

1. **Pick an Issue:** Review open issues in the `ISSUES.md` list or GitLab issue tracker. Assign yourself to an issue before starting work.
2. **Create a Feature Branch:** Always work on a separate branch. Name it based on the feature or issue:
   ```bash
   git checkout -b feature/issue-id-short-description
   ```
3. **Commit Messages:** Write clear, concise commit messages. Prefix with the issue number if applicable:
   ```bash
   git commit -m "#5: Implement PDF parser backend using PyMuPDF"
   ```
4. **Pull/Merge Requests:** Once ready, push your branch and open a Merge Request (MR) in GitLab against the `main` branch.

## Code Quality & Style

We use the following tools to maintain code quality:

* **Formatter:** Ruff (`ruff format .`)
* **Linter:** Ruff (`ruff check .`)
* **Type Checker:** MyPy (`mypy .`)
* **Tests:** PyTest (`pytest`)

Before submitting a Merge Request, run:
```bash
ruff format .
ruff check .
mypy .
pytest
```
Ensure all checks pass and there are no type errors or failing tests.

## Code Review & Merge

* Every Merge Request must be reviewed and approved by the other team member.
* Ensure all GitLab CI/CD runner checks pass before merging.
* Keep merge requests small and focused on a single task.
