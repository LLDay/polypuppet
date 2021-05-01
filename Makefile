SHELL := /bin/bash
PUPPET_CONF_DIR = '/etc/puppetlabs'

.PHONY: server agent clean

server:
	./scripts/install_server.sh
	python3 -m pip install .
	polypuppet setup server

agent:
	./scripts/install_agent.sh
	python3 -m pip install .
	polypuppet setup agent
