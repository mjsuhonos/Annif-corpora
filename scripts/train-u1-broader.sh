#!/bin/bash

#
# warning: Unknown subject URI
#
# large number of wikidata:instances

#poetry run annif train u1-broader-tfidf-en fulltext/uP279_P910_P921o_P31o/train
#poetry run annif train u1-broader-stwfsa-en fulltext/uP279_P910_P921o_P31o/train
#poetry run annif train u1-broader-mllm-en fulltext/uP279_P910_P921o_P31o/train
#poetry run annif train u1-broader-P31o-mllm-en fulltext/P31o/train
#poetry run annif train u1-broader-P921o-mllm-en fulltext/P921o/train
#poetry run annif train u1-broader-P279-mllm-en fulltext/P279/train
#poetry run annif train u1-broader-P910-mllm-en fulltext/P910/train
#
# train ensembles for combined NN
#

poetry run annif train u1-broader-nn-mllm-en fulltext/uP279_P910_P921o_P31o/test
poetry run annif train u1-broader-nn-combined-en fulltext/uP279_P910_P921o_P31o/test
