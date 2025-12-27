#! /bin/bash

curl -s https://www.wikidata.org/wiki/$1 | rg wikibase-title-label | sed -E 's/(<span class="wikibase-title-label">([^<]+)<\/span>[\n\r]*)*/"\2"/g' | uniq | jq