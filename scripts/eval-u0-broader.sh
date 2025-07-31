#!/bin/bash

poetry run annif eval -M u0-broader-stwfsa.json u0-broader-stwfsa-en fulltext/uP214_P227_P244_P268/eval
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:STWFSA"

#poetry run annif eval -M u0-broader-mllm.json u0-broader-mllm-en fulltext/uP214_P227_P244_P268/eval
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:MLLM"

#poetry run annif eval -M u0-broader-nn.json u0-broader-nn-ensemble-en fulltext/uP214_P227_P244_P268/eval
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:NN_ENSEMBLE"
