#!/bin/bash
Model="$1"
Model_id="$2"
tf_or_sess="$3"
dataset="$4"
python ./PPTC/main.py --test --dataset=long --model=gpt-4o-mini --sess --second --model_id=0000
python ./PPTC/main.py --eval --dataset=short --sess --model=gpt-4o-mini
