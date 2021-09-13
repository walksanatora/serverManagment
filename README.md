## Server Managment
##### *why did i make this*

Dependicies are in requirements.txt

## running
there are two ways, directly (reccommended)
`python3 main.py`<br>
or by using the make file
`make run`<br>

there are also some flags you can find by running `python3 main.py -h`
the makefile also contains some commands for resetting data and testing endpoints

## valid make targets
`make clean` - clears data and docker containers/volumes *for the entire system* (too lazy to be bothered)
`make image` - makes the docker images using the makefile in /containers
`make list` - list targets in the makefile
`make full-test` - runs the full-test.py file using python3.9
`make RMdata` - runs clearData.py using python3.9
`make RMcontainers` - runs purge-docker.py using python3.9
`make run` - runs main.py using python3.9
`make run-debug` - runs main.py using python3.9 with the -d arg

