#!/bin/bash


#
# uri2labels
#
# get the contents of a URI
# strip out the body text
# get label suggestions
# 

# $1 - URL to assign labels for
# $2 - URL to Annif instance, eg. http://localhost:5000/v1/projects/myproject/suggest

curl -ks $1 | \
readability $1 | \
lynx -stdin -dump -nolist |  \
iconv -f UTF-8 -t UTF-8//IGNORE | \
curl -s -X POST -H "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "limit=3" \
--data-urlencode "text@-" http://192.168.1.107:5000/v1/projects/u1-broader-e-arch0-en/suggest \
| jq 'del(..|nulls)'

#--data-urlencode "text@-" $2
