#!/bin/bash

# set environment variable for host IP
export DOCKER_HOST=ssh://root@`doctl compute droplet list --format "Name,PublicIPv4" | grep docker-annif | sed 's/[a-zA-Z<>/ :-]//g'`

echo ' ==> Evaluating backends...'

echo ' ==> backend: tf-idf'
docker exec -u root:root annif_bash_1 annif eval rula-tfidf-en Annif-corpora/fulltext/rula/test/ -v DEBUG

echo ' ==> backend: maui'
docker exec -u root:root annif_bash_1 annif eval rula-maui-en Annif-corpora/fulltext/rula/test/ -v DEBUG

echo ' ==> backend: omikuji-parabel'
docker exec -u root:root annif_bash_1 annif eval rula-omikuji-parabel-en Annif-corpora/fulltext/rula/test/ -v DEBUG

echo ' ==> backend: nn-ensemble'
docker exec -u root:root annif_bash_1 annif eval rula-triple-ensemble-en Annif-corpora/fulltext/rula/test/ -v DEBUG

echo ' ==> backend: (simple) ensemble'
docker exec -u root:root annif_bash_1 annif eval rula-ensemble-en Annif-corpora/fulltext/rula/test/ -v DEBUG

# unset environment variable for host IP
unset DOCKER_HOST
