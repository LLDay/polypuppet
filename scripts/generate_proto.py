from subprocess import call

command = 'protoc --python_out=polypuppet/ polypuppet.proto'
call(command.split())
