#!/bin/sh

ROOT=$(dirname "${0}")

docker stack deploy --compose-file "${ROOT}/docker-compose.yaml" web
