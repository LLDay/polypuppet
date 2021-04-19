#!/usr/bin/env bash

BASEDIR=$(dirname $0)
protoc --python_out="$BASEDIR/../polypuppet/" --proto_path "$BASEDIR/../" polypuppet.proto
