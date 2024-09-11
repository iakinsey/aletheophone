PYTHONPATH := .

test:
	@PYTHONPATH=$(PYTHONPATH) pytest

run:
	python -m aletheophone.main
