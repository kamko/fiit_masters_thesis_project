#!/usr/bin/env bash
timestamp=date-$(date +"%m-%d-%Y-%H_%M_%S")
uri=$1

file=monant-sync-dump-${timestamp}.sql.gz
pg_version="12.0"

mkdir -p backup

echo "Dumping data from ${uri}"
docker run --rm -i \
    postgres:${pg_version} \
    pg_dump --clean ${uri} | gzip -9 > ./backup/${file}


echo "Done"
