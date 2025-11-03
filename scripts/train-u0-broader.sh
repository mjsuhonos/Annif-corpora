#!/bin/bash

poetry run annif train u0-broader-tfidf-en fulltext/uP214_P227_P244_P268/train
poetry run annif train u0-broader-stwfsa-en fulltext/uP214_P227_P244_P268/train
poetry run annif train u0-broader-P214A-mllm-en fulltext/P214A/train
poetry run annif train u0-broader-P214B-mllm-en fulltext/P214B/train
poetry run annif train u0-broader-P227-mllm-en fulltext/P227/train
poetry run annif train u0-broader-P244-mllm-en fulltext/P244/train
poetry run annif train u0-broader-P268-mllm-en fulltext/P268/train
poetry run annif train u0-broader-nn-ensemble-en fulltext/uP214_P227_P244_P268/test
