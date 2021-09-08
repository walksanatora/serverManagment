# The setState endpoint

full path: /server/<id\>/setState
## request types and responses

headers:<br>
`Status`: int - server state as defined on the [server](/docs/server) page

status:     
`200` - request finished successfully <br>

upon a `*` request to this endpoint, the servers state updated 