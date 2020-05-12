#!/bin/bash
# Author: Josh Meyer, 2020
# must run within DeepSpeech dir with a venv set up

TO_DECODE_CSV=$1
DS_CHECKPOINT=$2

source venv/bin/activate
python evaluate.py \
       --test_files "${TO_DECODE_CSV}" \
       --checkpoint_dir "${DS_CHECKPOINT}" \
       --test_output_file "${TO_DECODE_CSV}-decoded.json" \
       --test_batch_size 1024 \
       --scorer "";
