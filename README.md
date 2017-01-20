# API docs

endpoint: `https://seed-project-v1.appspot.com/api/v1`

all json except `/images`

###users:
`POST /users`
params:  email, password

`GET /users/{id}`

`POST /tokens`

params: email, password

set the token to header with X-WALKER-ACCESS-TOKEN

###files:
`POST /files`

using multipart

params: file, file_type

file_type: 'file|image'

description: if file_type == image, serving_url will be provided, otherwise
download url via: `http://storage.googleapis.com/{gcs_path}`

##Change logs
### 2016-10-01
`POST /images` -> `POST /files`


## deleted
###images:
`POST /images`
