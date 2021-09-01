# The putFile endpoint

full path: /server/<id\>/putFile
## request types and responses

headers:
`file` - the path to the file (ex: 'testFile.txt)<br>
`content` - string representation of the file content

status:     
`200` - request finished successfully <br>

upon a `*` request to this endpoint, the file name and contents