# The setPort endpoint

full path: /server/<id\>/setPort
## request types and responses

headers:<br>
`HostPort`: int - the port on the physical machine<br>
`ContPort`: int - the port in the container<br>

status:     
`200` - request finished successfully <br>

upon a `*` request to this endpoint, the hostport and the containerport in the format `Container: Host`<br>
Note: reccomended to run [reloadContainer](/docs/server/id/reloadContainer) after changing ports for ports to be fowarded