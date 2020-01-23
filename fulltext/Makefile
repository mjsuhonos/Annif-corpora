# TODO: delete PDF and XML files ?

all: pdf txt xml key

# variables
pdf: $(patsubst %.tgz,%.pdf,$(wildcard */*.tgz))
txt: $(patsubst %.pdf,%.txt,$(wildcard */*.pdf))
xml: $(patsubst %.tgz,%.xml,$(wildcard */*.tgz))
key: $(patsubst %.xml,%.key,$(wildcard */*.xml))

# extract PDF files from TGZ files and save in same folder
%.pdf: %.tgz
	gtar -zxf $< --strip-components=2 --wildcards "*OBJ.pdf" && mv OBJ.pdf $@

# read PDF with pdftotext > output to PID.txt
# TODO: some PDFs refuse to be read on licensing grounds
%.txt: %.pdf
	pdftotext $< $(addprefix $(dir $@), $(subst Bag-RULA_,,$(notdir $@))) || true

# extract XML files from TGZ files and save in same folder
%.xml: %.tgz
	gtar -zxf $< --strip-components=2 --wildcards "*MODS.xml" && mv MODS.xml $@ || true
	gtar -zxf $< --strip-components=2 --wildcards "*MODS.bin" && mv MODS.bin $@ || true

# read XML with xsltproc > output to PID.key subjects (one per line)
# TODO: some transforms produce no subjects
%.key: %.xml
	xsltproc subjects.xslt $< > $(addprefix $(dir $@), $(subst Bag-RULA_,,$(notdir $@)))

# sed -i '' '/^\s* *$/d' *.key
# sed -i '' 's/ -- /--/g' *.key

.PHONY: all pdf txt xml key
