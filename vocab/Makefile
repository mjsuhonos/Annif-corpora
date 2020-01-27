all: nt gz

nt: $(patsubst %.skos,%.nt,$(wildcard */*.skos))
gz: $(patsubst %.nt,%.gz,$(wildcard */*.nt))

# extract prefLabel statements for id.loc.gov URIs
%.nt: %.skos
	cat $< | grep -F "http://www.w3.org/2004/02/skos/core#prefLabel" | grep -F "http://id.loc.gov/" > $@

%.gz: %.nt
	cat $< | parallel -l4000000 --pipe --block 600M pigz ">"{#}.gz

.PHONY: all nt gz