#!/bin/bash

## Author: Josh Meyer 2020
## this script takes as input a the original transcripts which have been
## exported from Excel as tilde-separated (~), with all new-lines already
## replaced with just a single space

## The script cleans up all known encoding errors, as well as removes
## extra-linguistic tags (um, laughter, part, en)

## Some of the encoding errors come from foreign words and names, where
## some diacritic was over a vowel, these have been changed to the base vowel
## e.g. "√∂" --> "o", instead of "ö"

CSV=$1

if [ ! -f "$CSV" ]; then
    echo "usage: ./clean-transcripts.sh transcripts.csv";
    exit 1;
fi

cat $CSV | \
    tr "~" "\t" | \
    cut -f2,3,5 | \
    tr '[A-Z]' '[a-z]' | \
    sed 's/https:\/\///g' | \
    sed 's/[aA-zZ]://g' | \
    sed 's/\[laughter*\]*//g' | \
    sed 's/\[um*\]*//g' | \
    sed 's/\[part\]//g' | \
    sed 's/\[\+\+part\]//g' | \
    sed 's/\[en\]//g' | \
    sed 's/\[p\]*//g' | \
    sed 's/\[hes\]//g' | \
    sed 's/\&/and/g' | \
    sed 's/\/ / /g' | \
    sed "s/Äô/\'/g" | \
    sed 's/√∂/o/g' | \
    sed 's/√≠/i/g' | \
    sed 's/ƒÅ/a/g' | \
    tr '©' 'e' | \
    tr "º\`" "'" | \
    tr -d '‚,\\|:?+][' | \
    tr -s ' ' \
       > all.csv

# get rid of the periods from the transcripts only, not the filenames
paste <(cut -f1,2 all.csv) <(cut -f3 all.csv|tr -d '.'|tr -s ' ') | sort | uniq > all.no-periods.uniq.csv
