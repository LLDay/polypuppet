SHELL := /bin/bash

.PHONY: server agent
.SILENT: agent server

server:
	./scripts/setup_server.sh
	python3 -m pip install .

agent:
ifeq "$(OS)" "Windows_NT"
	./scripts/setup_agent.ps1
	py -m pip install .
else
	./scripts/setup_agent.sh
	python3 -m pip install .
endif
