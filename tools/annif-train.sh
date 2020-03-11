#!/bin/bash

# set environment variable for host IP
export DOCKER_HOST=ssh://root@`doctl compute droplet list --format "Name,PublicIPv4" | grep docker-host | sed 's/[a-zA-Z<>/ :-]//g'`

echo 'Loading vocabularies...'

# Load vocabularies
time docker exec -u root:root annif_bash_1 annif loadvoc rula-maui-en Annif-corpora/vocab/rula/rula-lcsh-nogf.ttl

echo 'Training backends...'

# Train individual backends in sequence
time docker exec -u root:root annif_bash_1 annif train rula-tfidf-en Annif-corpora/training/rula.tsv.gz -v DEBUG
time docker exec -u root:root annif_bash_1 annif train rula-omikuji-parabel-en Annif-corpora/training/rula.tsv.gz -v DEBUG

time docker exec -u root:root annif_bash_1 annif train rula-maui-en Annif-corpora/fulltext/rula/1000/ -v DEBUG
time docker exec -u root:root annif_bash_1 annif train rula-triple-ensemble-en Annif-corpora/fulltext/rula/1000/ -v DEBUG

# unset environment variable for host IP
unset DOCKER_HOST
