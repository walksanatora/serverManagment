# The server endpoint

## states
each server has various states it can bein and here they are explained

0 - uninitilazed, blank server with nothing installed

1 - initiliazed, server has software installed

2 - starting, server is in the process of starting up

3 - running, server is currently active (various new endpoints become avaliable)

4 - stopping, server is in the process of shutting down


## request types and responses

- post

inputs:     `authToken` - the server auth token

outputs:    `key` - the key used to controll the server
            `id` - the id used to acess the server

status:     `403` - invalid `authToken` passed (invalid or missing)
            `200` - success server created

