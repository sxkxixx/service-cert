alembic-revision:
	alembic revision --autogenerate

alembic-upgrade-head:
	alembic upgrade head

lint:
	ruff check

format:
	ruff format