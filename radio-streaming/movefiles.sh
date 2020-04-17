#!/bin/bash
find radio_files -type f -maxdepth 1 -name "*.mp3" -exec mv {} radio_files/recorded \;
