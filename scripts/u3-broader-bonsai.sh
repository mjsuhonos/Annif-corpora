#!/bin/bash

poetry run annif train u3-broader-bonsai-en fulltext/uP279_P910_P361/train
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:BONSAI"

poetry run annif eval u3-broader-bonsai-en fulltext/uP279_P910_P361/eval
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:BONSAI"
