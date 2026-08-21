MAIN = main.py
RM = rm -rf
FLAGS = --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs


install:
	@uv sync -q

run: install
	@uv run python $(MAIN)

debug: install
	@uv run python -m pdb $(MAIN)

clean:
	@find . -type d -name "__pycache__" -exec $(RM) {} +
	@find . -type d -name ".mypy_cache" -exec $(RM) {} +

fclean: clean
	@$(RM) .venv

lint: install
	@uv run flake8 . --exclude=.venv
	@uv run mypy . $(FLAGS) --exclude="^\.venv"

lint-strict: install
	@uv run flake8 . --exclude=.venv
	@uv run mypy . --strict --exclude="^\.venv"

.PHONY: install run debug clean fclean lint lint-strict

