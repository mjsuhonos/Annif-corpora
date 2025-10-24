#!/bin/bash

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
