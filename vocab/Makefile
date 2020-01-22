all: nt

# variables
nt: $(patsubst %.skos,%.nt,$(wildcard *.skos))

# strip unnecessary statements from SKOS vocabularies
%.nt: %.skos
	cat $< | \
	grep -v "_:bnode" | \
	grep -v "http://www.w3.org/2008/05/skos-xl\#" | \
	grep -v "http://www.w3.org/2004/02/skos/core\#closeMatch" | \
	grep -v "http://www.w3.org/2004/02/skos/core\#inScheme" | \
	grep -v "http://www.w3.org/2004/02/skos/core\#note" | \
	grep -v "http://www.w3.org/2004/02/skos/core\#editorial" | \
	grep -v "http://www.w3.org/1999/02/22-rdf-syntax-ns\#type" | \
	> $@

.PHONY: all nt