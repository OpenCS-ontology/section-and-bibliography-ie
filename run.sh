#!/bin/bash
echo "Parsing $1"
python $(dirname "$0")/doc2json/grobid2json/process_pdf.py -i $1 -t $(dirname "$0")/temp -o $(dirname "$1")
echo "PDF -> JSON done"
python $(dirname "$0")/parse_json.py "${1%.*}.json"
echo "JSON -> TTL done"
rm "${1%.*}.json"
rm -R $(dirname "$0")/temp
echo "Done cleaning"
