# The lsFiles endpoint

full path: /server/<id\>/lsFiles
## request types and responses

status:     
`200` - request finished successfully <br>

upon a `*` request to this endpoint, will return json via `tree -J /mnt/data`