compile-requirements: requirements.txt requirements-dev.txt

requirements.txt: requirements.in
	pip-compile --strip-extras

requirements-dev.txt: requirements-dev.in
	pip-compile --strip-extras $<

install-requirements: requirements.txt
	pip install -r $<

install-dev-requirements: requirements-dev.txt
	pip install -r $<

sync-production-requirements: requirements.txt
	pip-sync $<

sync-dev-requirements: requirements.txt requirements-dev.txt
	pip-sync $?
