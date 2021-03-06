#!/bin/bash

echo ' ==> Evaluating backend: maui'
docker exec -u root:root annif_bash_1 annif eval rula-maui-en Annif-corpora/fulltext/rula/test/

echo ' ==> Evaluating backend: tf-idf'
docker exec -u root:root annif_bash_1 annif eval rula-tfidf-en Annif-corpora/fulltext/rula/test/

echo ' ==> Evaluating backend: omikuji-parabel'
docker exec -u root:root annif_bash_1 annif eval rula-omikuji-parabel-en Annif-corpora/fulltext/rula/test/

echo ' ==> Evaluating backend: fasttext'
docker exec -u root:root annif_bash_1 annif eval rula-fasttext-en Annif-corpora/fulltext/rula/test/

echo ' ==> Evaluating backend: nn-ensemble'
docker exec -u root:root annif_bash_1 annif eval rula-nn-ensemble-en Annif-corpora/fulltext/rula/test/
