check:
	pep8 pydiff pydiff.py setup.py
	pep257 pydiff pydiff.py setup.py
	pylint \
		--reports=no \
		--msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' \
		--disable=C0103,E1103 \
		--rcfile=/dev/null \
		pydiff.py setup.py
	check-manifest
	python setup.py --long-description | rstcheck -
	scspell pydiff pydiff.py setup.py test_pydiff.py README.rst

readme:
	@restview --long-description --strict
