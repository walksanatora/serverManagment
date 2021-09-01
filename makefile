clean: data docker

data:
	python3.8 clearData.py
docker:
	python3.8 purge-docker.py
