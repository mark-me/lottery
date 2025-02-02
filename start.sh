#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source ".venv/bin/activate"
python ./src/main.py
deactivate