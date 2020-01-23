all: nt ttl

nt: $(patsubst %.skos,%.nt,$(wildcard */*.skos))
ttl: $(patsubst %.nt,%.ttl,$(wildcard */*.nt))

# extract prefLabel statements for id.loc.gov URIs
%.nt: %.skos
	cat $< | grep -F "http://www.w3.org/2004/02/skos/core#prefLabel" | grep -F "http://id.loc.gov/" | sort | uniq > $@

%.ttl: %.nt
	rapper -i ntriples -o turtle -f 'xmlns:skos="http://www.w3.org/2004/02/skos/core#"' -f 'xmlns:lcsh="http://id.loc.gov/authorities/subjects/"' -f 'xmlns:lcgf="http://id.loc.gov/authorities/genreForms/"' -f 'xmlns:lcna="http://id.loc.gov/authorities/names/"' $< > $@

.PHONY: all nt ttl