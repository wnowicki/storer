# Contributing

## General

- Dependencies and project: [uv](https://docs.astral.sh/uv)
- Lint and format: [ruff](https://docs.astral.sh/ruff)
- Unit tests: [pytest](https://docs.pytest.org/en/stable/)

## Pre Commit

```shell
pre-commit install
```

For more information check [pre-commit](https://pre-commit.com/)

## Pull Requests

- Keep changes focused and small when possible.
- Add or update tests when behaviour changes.
- Update documentation when commands or behaviour change.
- Ensure linting and tests pass before opening a pull request.

## Setup

This project runs on `uv` please make sure you have it [installed](https://docs.astral.sh/uv/getting-started/installation/)

### Database Migrations

We are using [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) for migrations

#### Run Migrations

```shell
uv run alembic upgrade head 
```

#### Adding New Migration

Autogenerate new migration:

```shell
uv run alembic revision --autogenerate -m "MIGRATION_NAME"
```
