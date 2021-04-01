SHELL := /bin/bash

.PHONY: server agent clean

server:
	python3 ./scripts/generate_proto.py
	./scripts/install_server.sh

agent:
	python3 ./scripts/generate_proto.py
	./scripts/install_agent.sh
