
.PHONY: test cover

url = 

test:
	@python test.py $(url)

cover:
	coverage run coverage_test.py
	coverage html