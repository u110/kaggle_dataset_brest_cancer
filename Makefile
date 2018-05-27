setup: env pip

env:
	python -m virtualenv env -p python3

pip:
	env/bin/pip install -r requirements.txt

run-jupyter: jupyter-config nb-extensions
	env/bin/jupyter notebook

nb-extensions: ~/.jupyter/jupyter_notebook_config.py
	env/bin/jupyter contrib nbextension install --user

jupyter-config: ~/.jupyter/jupyter_notebook_config.py
	cp conf/jupyter_notebook_config.py ~/.jupyter/

~/.jupyter/jupyter_notebook_config.py: ~/.jupyter
	mv ~/.jupyter/jupyter_notebook_config.py{,.origin}

~/.jupyter:
	mkdir ~/.jupyter
