py = 'python3.9'
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

clean: data docker

image:
	@docker build -t 'cont' ${current_dir}/container

list:
	@grep '^[^#[:space:]].*:' makefile

full-test:
	${py} full-test.py

data:
	${py} clearData.py

docker:
	${py} purge-docker.py

run:
	${py} main.py

run-debug:
	${py} main.py -d
