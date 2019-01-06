#!/bin/sh

echo "Training experiment"

python --version

export PATH=$PATH:/usr/local/nvidia/bin

nvidia-smi

input_path="/data"
output_path=$(python -c "from polyaxon_client.tracking import get_outputs_path; print(get_outputs_path())")

echo ${input_path}

echo ${output_path}

cd cifar_10 && python cifar10_train_playground.py \
    --dataset_path=${input_path} \
    --output=${output_path} \
    --batch_size=256 \
    --val_batch_size=256 \
    --num_workers=16 \
    --model=resnet50_v2
