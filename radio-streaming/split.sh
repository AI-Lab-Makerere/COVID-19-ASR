#!/bin/bash
for file in *.mp3; do sox "$file" "n_$file" trim 0 300 : newfile : restart ; done
