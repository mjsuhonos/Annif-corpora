#!/bin/bash

# set environment variable for host IP
export DOCKER_HOST=ssh://root@`doctl compute droplet list --format "Name,PublicIPv4" | grep docker-host | sed 's/[a-zA-Z<>/ :-]//g'`

echo 'Evaluating backends...'

docker exec -u root:root annif_bash_1 annif eval rula-tfidf-en Annif-corpora/fulltext/islandora/test/ -v DEBUG
docker exec -u root:root annif_bash_1 annif eval rula-maui-en Annif-corpora/fulltext/islandora/test/ -v DEBUG
docker exec -u root:root annif_bash_1 annif eval rula-omikuji-parabel-en Annif-corpora/fulltext/islandora/test/ -v DEBUG
docker exec -u root:root annif_bash_1 annif eval rula-triple-ensemble-en Annif-corpora/fulltext/islandora/test/ -v DEBUG

# unset environment variable for host IP
unset DOCKER_HOST
