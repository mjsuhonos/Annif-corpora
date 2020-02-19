#!/bin/bash

# set environment variable for host IP
export DOCKER_HOST=ssh://root@`doctl compute droplet list --format "Name,PublicIPv4" | grep docker-host | sed 's/[a-zA-Z<>/ :-]//g'`

echo 'Training backends...'

# Load vocabularies
docker exec -u root:root annif_bash_1 annif loadvoc rula-tfidf-en Annif-corpora/vocab/lcsh/lcsh.ttl -v DEBUG

# Train individual backends in parallel
#docker exec -d -u root:root annif_bash_1 annif train rula-maui-en Annif-corpora/fulltext/islandora/validate/
#docker exec -d -u root:root annif_bash_1 annif train rula-tfidf-en Annif-corpora/fulltext/islandora/train/
#docker exec -d -u root:root annif_bash_1 annif train rula-omikuji-parabel-en Annif-corpora/fulltext/islandora/train/
#docker exec -d -u root:root annif_bash_1 annif train rula-triple-ensemble-en Annif-corpora/fulltext/islandora/train/

docker run -d -u root:root -v /mnt/annif_data:/annif-projects quay.io/natlibfi/annif \
	--name rula-maui-en annif train rula-maui-en Annif-corpora/fulltext/islandora/validate/

docker run -d -u root:root -v /mnt/annif_data:/annif-projects quay.io/natlibfi/annif \
	--name rula-tfidf-en annif train rula-tfidf-en Annif-corpora/fulltext/islandora/train/

docker run -d -u root:root -v /mnt/annif_data:/annif-projects quay.io/natlibfi/annif \
	--name rula-omikuji-parabel-en annif train rula-omikuji-parabel-en Annif-corpora/fulltext/islandora/train/

# Wait until training is done
time docker wait rula-tfidf-en
time docker wait rula-maui-en
time docker wait rula-omikuji-parabel-en

# Train ensemble backend
time docker exec -u root:root annif_bash_1 annif train rula-triple-ensemble-en Annif-corpora/fulltext/islandora/train/ -v DEBUG

# unset environment variable for host IP
unset DOCKER_HOST
