SHELL := /bin/bash

.PHONY: server agent clean
.SILENT: agent server

server:
	./scripts/setup_server.sh
	python3 -m pip install .
	install -m644 ./systemd/polypuppet.service /etc/systemd/system/

agent:
ifeq "$(OS)" "Windows_NT"
	./scripts/setup_agent.ps1
else
	./scripts/setup_agent.sh
endif
	python3 -m pip install .
