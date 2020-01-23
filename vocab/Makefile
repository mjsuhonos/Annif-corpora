all: nt

nt: $(patsubst %.skos,%.nt,$(wildcard */*.skos))

# extract prefLabel and altLabel statements
# TODO: use ripgrep if it's present
%.nt: %.skos
	grep -F "http://id.loc.gov/" | grep -F "http://www.w3.org/2004/02/skos/core#prefLabel" $< > prefLabel-$@
	grep -F "http://id.loc.gov/" | grep -F "http://www.w3.org/2004/02/skos/core#altLabel"  $< > altLabel-$@

.PHONY: all nt