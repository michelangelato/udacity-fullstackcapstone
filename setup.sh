#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/cinema"
export EXCITED="true"
echo "env variable setted executed successfully!"
createdb cinema
echo "database created successfully!"