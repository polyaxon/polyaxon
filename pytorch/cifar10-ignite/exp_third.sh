#!/bin/sh

echo "Another experiment"

python --version

python check.py

export PATH=$PATH:/usr/local/nvidia/bin

nvidia-smi

python check_plx_logging.py
