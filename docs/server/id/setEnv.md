# The setEnv endpoint

full path: /server/<id\>/setEnv
## request types and responses

headers:<br>
`Key`: str - the key that will be set<br>
`Value`: str - the value that will be set<br>

status:     
`200` - request finished successfully <br>

upon a `*` request to this endpoint, key and value in json form