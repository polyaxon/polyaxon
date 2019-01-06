#!/bin/sh

echo "Another experiment"

python --version

python check.py

export PATH=$PATH:/usr/local/nvidia/bin

nvidia-smi

input_path="/data"
output_path=$(python -c "from polyaxon_client.tracking import get_outputs_path; print(get_outputs_path())")

echo ${input_path}

echo ${output_path}

ls *
