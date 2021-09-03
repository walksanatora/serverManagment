# The server endpoint

## states
each server has various states it can bein and here they are explained

0 - uninitilazed, blank server with nothing installed

1 - initiliazed, server has software installed

2 - starting, server is in the process of starting up

3 - running, server is currently active (various new endpoints become avaliable)

4 - stopping, server is in the process of shutting down


## internal server values
`Name`: str - the server name (cannot be changed)<br>
`State`: int - server state (see above)

## request types and responses

- post

inputs:<br>     `authToken` - the server auth token<br>
            `opt` - a json-serialized to set default internal variables

outputs:<br>    `key` - the key used to controll the server<br>
            `id` - the id used to acess the server

status:<br>     `403` - invalid `authToken` passed (invalid or missing)<br>
            `200` - success server created

