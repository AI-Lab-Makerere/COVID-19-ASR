#!/bin/bash
# Author: Josh Meyer, 2020
MP3=$1

cd py-webrtcvad # https://github.com/wiseman/py-webrtcvad.git
./vad-and-selection.sh "${MP3}"
cd ../DeepSpeech # https://github.com/mozilla/DeepSpeech.git
./decode.sh "${MP3}-chunks/select/to-decode.csv"
./select-best-after-decoding.sh "${MP3}-chunks/select/to-decode.csv-decoded.json" "${INPUT}-chunks/lens.select"
