#!/bin/bash

for f in "$@"
do
    echo "Processing ${f}"
    if [ -f "${f}.csv" ]; then
        echo "CSV exists!"
    else
        .venv/bin/python scripts/formula_log_extract.py dbc/Megasquirt_CAN-2014-10-27.dbc "${f}" > "${f}.csv"
        .venv/bin/python scripts/power_buckets.py "${f}.csv"
    fi
done
