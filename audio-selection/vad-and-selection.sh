#!/bin/bash
# Author: Josh Meyer, 2020
# should be run from within py-webrtcvad with a venv already set up

# input == one mp3 file from S3
# output == directory of selected candidate audio files
#        == csv file formatted for deepspeech evaluate.py
#        == lens.select for select-best-after-decode.sh

INPUT=$1
mkdir ${INPUT}-chunks

ffmpeg -i $INPUT -ac 1 -ar 16k -ab 128k ${INPUT}.wav
source venv/bin/activate
python example.py 3 ${INPUT}.wav
mv chunk*wav ${INPUT}-chunks/.
cd ${INPUT}-chunks
for i in *wav; do echo $i $( soxi -D $i ) >> lens; done

grep " 2\." lens >> lens.select
grep " 3\." lens >> lens.select
grep " 4\." lens >> lens.select
grep " 5\." lens >> lens.select
grep " 6\." lens >> lens.select
grep " 7\." lens >> lens.select
grep " 8\." lens >> lens.select

cut lens.select -f1 -d' ' > lens.select.col
mkdir select

while read wav; do mv $wav select/$wav; done<lens.select.col

cat <( echo "wav_filename,wav_filesize,transcript" ) <( cat lens.select.col | sed -E 's/$/,0,foo/g' ) > select/to-decode.csv

echo "You can find your select chunks in ${INPUT}-chunks/select"
echo "You can find your CSV ready for DeepSpeech evaluate.py at ${INPUT}-chunks/select/to-decode.csv"
