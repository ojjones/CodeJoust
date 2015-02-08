#!/bin/sh
curl -H "Content-type: application/json" -d @compile_json http://localhost:8000/api/compile
