# monant-sync
[![image metadata](https://images.microbadger.com/badges/image/kamko/monant-sync.svg)](https://microbadger.com/images/kamko/monant-sync "kamko/monant-sync image metadata")

Automatic image builds and pushed to [Docker Hub](https://hub.docker.com/r/kamko/monant-sync).


## Run
Run using docker (so you don't need to care about dependencies)
```
docker run --rm kamko/monant-sync \
        -e MONANT_AUTH_USERNAME=<username> \
        -e MONANT_AUTH_PASSWORD=<password> \
        -e POSTGRESQL_URI=<pg-uri>\
        [OPTIONS] COMMAND [ARGS]...
```

