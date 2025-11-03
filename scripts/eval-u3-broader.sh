#!/bin/bash

#poetry run annif eval u3-broader-stwfsa-en fulltext/uP279_P910_P361/eval
#poetry run annif eval u3-broader-mllm-en fulltext/uP279_P910_P361/eval
#poetry run annif eval u3-broader-nn-ensemble-en fulltext/uP279_P910_P361/eval
poetry run annif eval -M u3-broader-nn-2.json u3-broader-nn-ensemble-2-en fulltext/uP279_P910_P361/eval
