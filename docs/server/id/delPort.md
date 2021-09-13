# The delPort endpoint

full path: /server/<id\>/delPort
## request types and responses

headers:<br>
`ContPort`: int - the port in the container<br>

status:     
`200` - request finished successfully <br>

upon a `*` request to this endpoint, the port that was removed<br>
Note: reccomended to run [reloadContainer](/docs/server/id/reloadContainer) after changing ports for ports to be fowarded