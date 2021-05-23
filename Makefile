SHELL := /bin/bash
PUPPET_CONF_DIR = '/etc/puppetlabs'

.PHONY: server agent clean

server:
	./scripts/setup_server.sh
	python3 -m pip install .
	install -m644 ./systemd/polypuppet.service /etc/systemd/system/

agent:
	./scripts/setup_agent.sh
	python3 -m pip install .
