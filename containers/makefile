all: alpine openjdk16

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

alpine:;@docker build -t 'alpine-srv' ${current_dir}/alpine-slim
openjdk16:;@docker build -t 'openjdk16-srv' ${current_dir}/openjdk-16