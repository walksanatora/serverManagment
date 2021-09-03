py = 'python3.9'

clean: data docker

list:
	@grep '^[^#[:space:]].*:' makefile

full-test:
	${py} full-test.py

data:
	${py} clearData.py

docker:
	${py} purge-docker.py
