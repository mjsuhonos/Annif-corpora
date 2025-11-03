#!/bin/bash

#poetry run annif train u3-broader-stwfsa-en fulltext/uP279_P910_P361/train
#poetry run annif train u3-broader-mllm-en fulltext/uP279_P910_P361/train
#poetry run annif train u3-broader-nn-ensemble-en fulltext/uP279_P910_P361/test
poetry run annif train u3-broader-P279-mllm-en fulltext/P279/train
poetry run annif train u3-broader-P361-mllm-en fulltext/P361/train
poetry run annif train u3-broader-P910-mllm-en fulltext/P910/train
poetry run annif train u3-broader-nn-ensemble-2-en fulltext/uP279_P910_P361/test
