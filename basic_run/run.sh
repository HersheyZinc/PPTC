#!/bin/bash
Model="$1"
Model_id="$2"
tf_or_sess="$3"
dataset="$4"
python3 ./PPT_code/main.py --test --dataset="$dataset" --model="$Model" --"$tf_or_sess" --resume --second --model_id="$Model_id"
# python ./PPTC/main.py --test --dataset=short --model=turbo --tf --resume --second --model_id=0000