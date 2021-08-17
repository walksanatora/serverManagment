# The server endpoint

## request types and responses

- post

inputs:     `authToken` - the server auth token

outputs:    `key` - the key used to controll the server
            `id` - the id used to acess the server

status:     `403` - invalid `authToken` passed (invalid or missing)
            `200` - success server created

