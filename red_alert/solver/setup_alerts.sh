PORT=locahost
HOST=12000

curl -u admin:spacemath -vX 'POST' \
  "http://${HOST}:${PORT}/api/ruler/grafana/api/v1/rules/Services" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @laser-off.json

curl -u admin:spacemath -vX 'POST' \
  "http://${HOST}:${PORT}/api/ruler/grafana/api/v1/rules/Services" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @laser-on.json

  
#curl -u admin:spacemath -vX 'POST' \
  #'http://localhost:3000/api/ruler/grafana/api/v1/rules/Services' \
  #-H 'accept: application/json' \
  #-H 'Content-Type: application/json' \
  #-d @safe.json

#curl -u admin:spacemath -vX 'POST' \
  #'http://localhost:3000/api/ruler/grafana/api/v1/rules/Services' \
  #-H 'accept: application/json' \
  #-H 'Content-Type: application/json' \
  #-d @detector-on.json
