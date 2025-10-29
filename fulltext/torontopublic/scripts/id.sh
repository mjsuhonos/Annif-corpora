#! /bin/bash

idloc get https://id.loc.gov/authorities/subjects/$1 | jq '.["skos:prefLabel"]["@value"]'