#!/bin/bash
set -e  # stop if any command fails

# install in editable mode from root
pip install -e .

# clean up old data
rm -rf pysubebm/test/my_data

# run generator from root
python3 pysubebm/test/gen.py
