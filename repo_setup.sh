#!/bin/bash
git clone https://github.com/allenai/s2orc-doc2json.git s2orc-doc2json
cd s2orc-doc2json
pip install -r requirements.txt
pip uninstall flask --yes
pip install flask rdflib
head -n -1 scripts/setup_grobid.sh > scripts/setup_grobid.sh.tmp && mv scripts/setup_grobid.sh.tmp scripts/setup_grobid.sh
chmod u+x scripts/*.sh
