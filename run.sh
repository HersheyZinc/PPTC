#!/bin/bash
Model="$1"
Model_id="$2"
tf_or_sess="$3"
dataset="$4"
python ./PPTC/main.py --test --dataset=short --model=gpt4o-mini --tf --second --model_id=0000 --planning
python ./PPTC/main.py --eval --dataset=short --tf --model=gpt4o-mini
