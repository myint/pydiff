check:
	pep8 pydiff pydiff.py setup.py
	pep257 pydiff pydiff.py setup.py
	pylint --report=no --include-ids=yes --disable=C0103,E1103,W0622 --rcfile=/dev/null pydiff.py setup.py
	check-manifest --ignore=.travis.yml,Makefile
	python setup.py --long-description | rst2html --strict > /dev/null
	scspell pydiff pydiff.py setup.py test_pydiff.py README.rst

readme:
	@restview --long-description --strict
