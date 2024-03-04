compile-requirements: requirements.txt

requirements.txt: requirements.in
	pip-compile --strip-extras

install-requirements:
	pip install -r requirements.txt

sync-requirements:
	pip-sync requirements.txt
