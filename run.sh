#!/bin/bash

python3 imgs2pdf.py $1
if [ $? -ne 0 ]; then
    open -t $1"/config.json"
fi
