#!/bin/bash

set -a
source config.env
set +a

# flask run --debug --host=0.0.0.0
python3.12 app.py

