#!/bin/bash

#poetry run annif eval u3-broader-stwfsa-en fulltext/uP279_P910_P361/eval
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:STWFSA"

#poetry run annif eval u3-broader-mllm-en fulltext/uP279_P910_P361/eval
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:MLLM"

#poetry run annif eval u3-broader-nn-ensemble-en fulltext/uP279_P910_P361/eval
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:NN_ENSEMBLE"

poetry run annif eval -M u3-broader-nn-2.json u3-broader-nn-ensemble-2-en fulltext/uP279_P910_P361/eval
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:NN_ENSEMBLE_2"
