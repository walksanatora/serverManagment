py = 'python3.9'
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

clean: RMdata RMdocker

image:
	@docker build -t 'cont' ${current_dir}/container

list:
	@grep '^[^#[:space:]].*:' makefile

full-test:
	${py} full-test.py

RMdata:
	${py} clearData.py

RMdocker:
	${py} purge-docker.py

run:
	${py} main.py

run-debug:
	${py} main.py -d
