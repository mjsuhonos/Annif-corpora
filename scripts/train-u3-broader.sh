#!/bin/bash

#poetry run annif train u3-broader-stwfsa-en fulltext/uP279_P910_P361/train
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:STWFSA"

#poetry run annif train u3-broader-mllm-en fulltext/uP279_P910_P361/train
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:MLLM"

#poetry run annif train u3-broader-nn-ensemble-en fulltext/uP279_P910_P361/test
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:NN_ENSEMBLE"

poetry run annif train u3-broader-P279-mllm-en fulltext/P279/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:MLLM_P279"

poetry run annif train u3-broader-P361-mllm-en fulltext/P361/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:MLLM_P361"

poetry run annif train u3-broader-P910-mllm-en fulltext/P910/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:MLLM_P910"

poetry run annif train u3-broader-nn-ensemble-2-en fulltext/uP279_P910_P361/test
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:NN_ENSEMBLE_2"
