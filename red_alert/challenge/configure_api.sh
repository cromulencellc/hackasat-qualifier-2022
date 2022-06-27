#! /bin/sh
# Configure users with some api commands
curl -u admin:spacemath -vX POST http://localhost:3000/api/admin/users -d @apicmds/users.json --header "Content-Type: application/json"
