#!/bin/bash

dna_dir="/data/DNA"

if [[ -f "$dna_dir/hosfix.zip" ]]; then
    aria2c -j 8 -x 8 -s 8 --summary-interval=1 --console-log-level=warn --download-result=hide --continue=true --auto-file-renaming=true -d "$dna_dir" -o "hosfix.zip" "https://github.com/Yustinia/POCOF4-Script/releases/download/1.0.0/hyperos3-fixes.zip"
fi

7z x "$dna_dir/hosfix.zip" -o"$dna_dir/hosfix"