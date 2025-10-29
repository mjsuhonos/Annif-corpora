#! /bin/bash

curl -s https://www.wikidata.org/wiki/$1 | rg wikibase-title-label