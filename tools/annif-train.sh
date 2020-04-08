#!/bin/bash

# set environment variable for host IP
export DOCKER_HOST=ssh://root@`doctl compute droplet list --format "Name,PublicIPv4" | grep docker-annif | sed 's/[a-zA-Z<>/ :-]//g'`

# Clear Annif to initial state
echo ' ==> Resetting Annif projects...'

docker exec -u root:root annif_bash_1 annif clear rula-tfidf-en
docker exec -u root:root annif_bash_1 annif clear rula-maui-en
docker exec -u root:root annif_bash_1 annif clear rula-omikuji-parabel-en
docker exec -u root:root annif_bash_1 annif clear rula-triple-ensemble-en

echo ' ==> Loading vocabularies...'
#time docker exec -u root:root annif_bash_1 annif loadvoc rula-maui-en Annif-corpora/vocab/rula/rula-lcsh.ttl

# Train individual backends in sequence
echo ' ==> Training backends...'

time docker exec -u root:root annif_bash_1 annif train rula-tfidf-en Annif-corpora/training/rula.tsv.gz -v DEBUG
time docker exec -u root:root annif_bash_1 annif train rula-maui-en Annif-corpora/fulltext/rula/1000/ -v DEBUG
time docker exec -u root:root annif_bash_1 annif train rula-omikuji-parabel-en Annif-corpora/training/rula.tsv.gz -v DEBUG
time docker exec -u root:root annif_bash_1 annif train rula-triple-ensemble-en Annif-corpora/fulltext/rula/1000/ -v DEBUG

# unset environment variable for host IP
unset DOCKER_HOST
