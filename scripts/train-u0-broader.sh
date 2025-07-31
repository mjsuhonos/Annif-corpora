#!/bin/bash

poetry run annif train u0-broader-tfidf-en fulltext/uP214_P227_P244_P268/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:TFIDF"

poetry run annif train u0-broader-stwfsa-en fulltext/uP214_P227_P244_P268/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:STWFSA"

poetry run annif train u0-broader-P214A-mllm-en fulltext/P214A/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:P214A_MLLM"

poetry run annif train u0-broader-P214B-mllm-en fulltext/P214B/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:P214B_MLLM"

poetry run annif train u0-broader-P227-mllm-en fulltext/P227/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:P227_MLLM"

poetry run annif train u0-broader-P244-mllm-en fulltext/P244/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:P244_MLLM"

poetry run annif train u0-broader-P268-mllm-en fulltext/P268/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:P268_MLLM"

poetry run annif train u0-broader-nn-ensemble-en fulltext/uP214_P227_P244_P268/test
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:NN_ENSEMBLE"
