SHELL := /bin/bash

.PHONY: server agent clean

server:
	./scripts/install_server.sh

agent:
	./scripts/install_agent.sh
