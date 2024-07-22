test: install
	pytest
lint: install
	flake8
run: install
	python tests/integration.py
release: install clean
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*
	$(MAKE) clean
clean:
	rm -rf dist build *.egg-info .eggs
install:
	pip install --quiet -r requirements/dev.txt
