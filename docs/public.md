# The public endpoint

full path: /public
## request types and responses

all endpoints after this point will have the following statuses and headers<br>
headers:    `authToken` - the auth token generated by the server at creation<br>

status:     
`400` - server doesen't exist <br>
`403` - invalid `authToken`<br>
`404` - endpoint not found

upon a `GET` request to this endpoint a full dump of the public volume will be created <br>
