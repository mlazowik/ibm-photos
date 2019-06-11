#!/bin/bash

docker run --name django-db -e POSTGRES_PASSWORD=django -d -p 5432:5432 postgres
