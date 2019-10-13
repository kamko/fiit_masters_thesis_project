#!/bin/bash

docker pull --quiet kamko/monant-sync
docker run --rm --env-file kmk-auth.env \
		kamko/monant-sync "$@"
