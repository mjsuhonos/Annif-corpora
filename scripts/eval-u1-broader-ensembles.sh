#!/bin/bash

#poetry run annif eval -M u1-broader-e-arch0.json u1-broader-e-arch0-en fulltext/uP279_P910_P921o_P31o/eval
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:ARCH0"

poetry run annif eval -M u1-broader-e-arch2.json u1-broader-e-combined-en fulltext/uP279_P910_P921o_P31o/eval
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:ARCH2"

#poetry run annif eval -M u1-broader-e-arch1.json u1-broader-e-arch0-en fulltext/uP279_P910_P921o_P31o/eval
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:ARCH1"

#poetry run annif eval -M u1-broader-e-arch3.json u1-broader-e-arch0-en fulltext/uP279_P910_P921o_P31o/eval
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=EVAL_COMPLETE:ARCH3"
