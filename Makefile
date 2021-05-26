SHELL := /bin/bash

.PHONY: server agent
.SILENT: agent server

server:
	./scripts/setup_server.sh
	python3 -m pip install .

agent:
	python3 -m pip install .
ifeq "$(OS)" "Windows_NT"
	./scripts/setup_agent.ps1
else
	./scripts/setup_agent.sh
endif
