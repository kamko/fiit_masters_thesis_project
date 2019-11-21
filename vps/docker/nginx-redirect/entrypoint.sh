#!/bin/bash

if [[ -z "$TARGET_HOST" ]]; then echo "TARGET_HOST is required!" && exit 1; fi

echo "Setting catch-all redirect to ${TARGET_HOST}"
envsubst '${TARGET_HOST}' < template.nginx > /etc/nginx/conf.d/default.conf

echo "Starting nginx"

nginx -g "daemon off;"
