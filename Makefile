setup: env pip

env:
	python -m virtualenv env -p python3

pip:
	env/bin/pip install -r requirements.txt

run-jupyter:
	env/bin/jupyter notebook
