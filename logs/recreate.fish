#!/usr/bin/env fish

./down.fish

docker compose up -d
# so I can detach and not stop containers
docker compose logs -f
