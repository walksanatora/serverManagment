# INDEX

### general information
all endpoints will return a json string with the following information

a `*` request indicates that any request will trigger the condition

`status` - the http status returned<br>
`message` - amessage explaining the http status<br>
`failed` - boolean saying whether the request failed <br>
`output` (only if failed is False) the kwarg outputs of the endpoint

### endpoints
* [server](/docs/server)<br>
* [public](/docs/public)<br>