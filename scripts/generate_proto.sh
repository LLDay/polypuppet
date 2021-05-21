#!/usr/bin/env bash

BASEDIR=$(dirname $0)
DIR="$BASEDIR/../polypuppet"

python3 -m grpc_tools.protoc --python_out="$DIR" --grpc_python_out="$DIR" --proto_path "$BASEDIR/../" polypuppet.proto
sed -i 's#import polypuppet_pb2#import polypuppet.polypuppet_pb2#g' "$DIR/polypuppet_pb2_grpc.py"
