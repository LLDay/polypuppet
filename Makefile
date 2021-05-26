SHELL := /bin/bash

.PHONY: server agent
.SILENT: agent server

server:
	python3 -m pip install .
	install -m644 ./systemd/polypuppet.service /etc/systemd/system/
	./scripts/setup_server.sh

agent:
	python3 -m pip install .
ifeq "$(OS)" "Windows_NT"
	./scripts/setup_agent.ps1
else
	./scripts/setup_agent.sh
endif
