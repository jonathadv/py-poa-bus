default: help

# Run pipenv install
install:
	pipenv install --dev

# Run pylint
lint:
	pipenv _run pylint ./setup.py pypoabus


# Run tests with pytest
test:
	pytest -s --verbose ./tests


# Run tests with pytest and coverage
test-cov:
	pytest -s --verbose --cov-report term-missing --cov=pypoabus ./tests


# Sort imports as PEP8
isort:
	pipenv _run isort **/*.py

# Display this help
help:
	@ echo
	@ echo '  Usage:'
	@ echo ''
	@ echo '	make <target> [flags...]'
	@ echo ''
	@ echo '  Targets:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?:/{ print "   ", $$1, comment }' ./Makefile | column -t -s ':' | sort
	@ echo ''
	@ echo '  Flags:'
	@ echo ''
	@ awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?\?=/{ print "   ", $$1, $$2, comment }' ./Makefile | column -t -s '?=' | sort
	@ echo ''
