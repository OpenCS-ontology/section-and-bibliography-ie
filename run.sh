#!/bin/bash
echo "Parsing $1"
python doc2json/grobid2json/process_pdf.py -i $1 -t $(dirname "$0")/temp -o $(dirname "$1")
echo "PDF -> JSON done"
python parse_json.py "${1%.*}.json"
echo "JSON -> TTL done"