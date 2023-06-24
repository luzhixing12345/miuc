
.PHONY: test cover

url = 

test:
	python -m miuc.main url

cover:
	coverage run coverage_test.py
	coverage html

build:
	pnpm vsce package --no-dependencies 

publish:
	pnpm vsce publish --no-dependencies