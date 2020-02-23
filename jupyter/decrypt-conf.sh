#!/bin/bash

sops --decrypt --input-type json --output-type json db-conf.json.enc > db-conf.json
