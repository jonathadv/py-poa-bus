default: help

# Run pipenv install
install:
	pipenv install --dev

# Run pylint
lint:
	pipenv run pylint ./setup.py pypoabus


# Run tests with pytest
test:
	pytest -s --verbose --durations=5 --cov=pypoabus ./tests


# Sort imports as PEP8
isort:
	pipenv run isort **/*.py

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
