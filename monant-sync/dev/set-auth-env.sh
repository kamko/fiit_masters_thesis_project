#!/bin/bash

set -e

auth_file=$1

if [[ -z "$auth_file" ]]; then echo "Missing 'auth_file' parameter" && exit 1; fi

auth=$(sops -d $auth_file)

while read -r line
    do 
        export "$line"
    done <<< $auth
