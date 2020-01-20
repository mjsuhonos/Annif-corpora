all: nt

# variables
nt: $(patsubst %.skos,%.nt,$(wildcard */*.skos))

# strip unnecessary statements from SKOS vocabularies
%.nt: %.skos
	cat $< | \
	sed '/changeset/d' | \
	sed '/changeNote/d' | \
	sed '/exactMatch/d' | \
	sed '/closeMatch/d' | \
	sed '/altLabel/d' | \
	sed '/broader/d' | \
	sed '/narrower/d' | \
	sed '/skos-xl/d' | \
	> $@

.PHONY: all nt