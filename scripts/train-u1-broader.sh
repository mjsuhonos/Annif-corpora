#!/bin/bash

#
# warning: Unknown subject URI
#
# large number of wikidata:instances

#poetry run annif train u1-broader-tfidf-en fulltext/uP279_P910_P921o_P31o/train
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:TFIDF"

#poetry run annif train u1-broader-stwfsa-en fulltext/uP279_P910_P921o_P31o/train
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:STWFSA"

#poetry run annif train u1-broader-mllm-en fulltext/uP279_P910_P921o_P31o/train
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:MLLM"

#poetry run annif train u1-broader-P31o-mllm-en fulltext/P31o/train
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:MLLM_P31o"

#poetry run annif train u1-broader-P921o-mllm-en fulltext/P921o/train
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:MLLM_P921o"

#poetry run annif train u1-broader-P279-mllm-en fulltext/P279/train
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:MLLM_P279"

#poetry run annif train u1-broader-P910-mllm-en fulltext/P910/train
#curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:MLLM_P910"

#
# train ensembles for combined NN
#

poetry run annif train u1-broader-nn-mllm-en fulltext/uP279_P910_P921o_P31o/test
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:NN_MLLM"

poetry run annif train u1-broader-nn-combined-en fulltext/uP279_P910_P921o_P31o/test
curl -XGET "https://voip.ms/api/v1/rest.php?api_username=mj@suhonos.ca&api_password=cohkeb-hawse4-Jyqnop&method=sendSMS&did=6478124729&dst=4168354981&message=TRAINING_COMPLETE:NN_COMBINED"
