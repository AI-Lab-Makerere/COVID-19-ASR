#!/bin/bash
# Author: Josh Meyer, 2020

INPUT=$1 # decoded.json from decode.sh
AUDIO_LENS=$2 # lens.select from vad-and-selection.sh

cat $INPUT | \
    jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' | \
    cut -d',' -f5,7 \
        >tmp.res

paste <( cat tmp.res | cut -d',' -f2 | tr -d '"' | rev | cut -d'/' -f1 | rev ) <( cat tmp.res | cut -d',' -f1 | awk '{ print length }' ) > tmp.res.len

join <( sort $AUDIO_LENS ) <( sort tmp.res.len ) > tmp.join

while read line; do echo $( echo $line | cut -d' ' -f1 ) $( echo "scale=2; $( echo $line | cut -d' ' -f3 ) / $( echo $line | cut -d' ' -f2 )" | bc ) >> tmp.score; done<tmp.join

sort -k2nr -o ${INPUT}.score tmp.score 

echo "your final ranking of files can be found in $INPUT.score"

