#!/bin/bash

# Clear Annif to initial state
echo ' ==> Resetting Annif projects...'

docker exec -u root:root annif_bash_1 annif clear rula-maui-en
docker exec -u root:root annif_bash_1 annif clear rula-tfidf-en
docker exec -u root:root annif_bash_1 annif clear rula-omikuji-parabel-en
docker exec -u root:root annif_bash_1 annif clear rula-fasttext-en
docker exec -u root:root annif_bash_1 annif clear rula-mllm-en
docker exec -u root:root annif_bash_1 annif clear rula-stwfsa-en
docker exec -u root:root annif_bash_1 annif clear rula-yake-en
docker exec -u root:root annif_bash_1 annif clear rula-vw-multi-en
docker exec -u root:root annif_bash_1 annif clear rula-svc-en
docker exec -u root:root annif_bash_1 annif clear rula-nn-ensemble-en

echo ' ==> Loading vocabularies...'
time docker exec -u root:root annif_bash_1 annif loadvoc rula-maui-en Annif-corpora/vocab/rula/rula-lcsh.ttl

# Train individual backends in sequence
echo ' ==> Training backends...'

time docker exec -u root:root annif_bash_1 annif train rula-maui-en Annif-corpora/fulltext/rula/1000/
time docker exec -u root:root annif_bash_1 annif train rula-tfidf-en Annif-corpora/training/rula.tsv.gz
time docker exec -u root:root annif_bash_1 annif train rula-omikuji-parabel-en Annif-corpora/training/rula.tsv.gz
time docker exec -u root:root annif_bash_1 annif train rula-fasttext-en Annif-corpora/training/rula.tsv.gz
time docker exec -u root:root annif_bash_1 annif train rula-mllm-en Annif-corpora/training/rula.tsv.gz
time docker exec -u root:root annif_bash_1 annif train rula-stwfsa-en Annif-corpora/training/rula.tsv.gz
time docker exec -u root:root annif_bash_1 annif train rula-vw-multi-en Annif-corpora/training/rula.tsv.gz
time docker exec -u root:root annif_bash_1 annif train rula-svc-en Annif-corpora/training/rula.tsv.gz
time docker exec -u root:root annif_bash_1 annif train rula-nn-ensemble-en Annif-corpora/fulltext/rula/1000/
