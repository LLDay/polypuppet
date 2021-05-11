SHELL := /bin/bash
PUPPET_CONF_DIR = '/etc/puppetlabs'

.PHONY: server agent clean

server:
	./scripts/setup_server.sh
	python3 -m pip install .

agent:
	./scripts/setup_agent.sh
	python3 -m pip install .
