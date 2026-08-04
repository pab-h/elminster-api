#!/bin/sh

set -e

docker exec -it elminster_garage /garage bucket website --allow elminster-bucket
docker exec -it elminster_api uv run alembic upgrade head
