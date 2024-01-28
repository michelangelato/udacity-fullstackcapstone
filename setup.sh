#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/cinema"
export EXCITED="true"
export AUTH0_DOMAIN="michelangelomarani.eu.auth0.com"
export API_AUDIENCE="cinema"
echo "env variable setted executed successfully!"
createdb cinema
echo "database created successfully!"