setup: env pip config-jupyter

env:
	python -m virtualenv env -p python3

pip:
	env/bin/pip install -r requirements.txt

run-jupyter:
	env/bin/jupyter notebook

nb-extensions:
	env/bin/jupyter contrib nbextension install --user

config-jupyter: nb-extensions backup-current-config
	cp conf/jupyter_notebook_config.py ~/.jupyter/

backup-current-config: ~/.jupyter/jupyter_notebook_config.py.BAK

~/.jupyter/jupyter_notebook_config.py.BAK: ~/.jupyter
	-mv -n ~/.jupyter/jupyter_notebook_config.py{,.BAK}

~/.jupyter:
	mkdir ~/.jupyter
