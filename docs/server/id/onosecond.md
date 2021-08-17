# The onosecond endpoint

## request types and responses

- ANY

inputs:     `authToken` - the server auth token

outputs:    all headers passed in json form

status:     `200` - endpoint worked
            `403` - invalid authToken
