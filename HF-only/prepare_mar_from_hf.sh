#!/bin/bash
HF_REPO_URL = ""
MODEL_NAME = ""
for arg in "$@"
do
    case $arg in
        -t|--task)
            sed -i "s/task=\".*/task=\"$2\"/g" scripts/torchserve_vitxxsmall_handler.py
            shift 2
            ;;
        -n|--model-name)
            MODEL_NAME="$2"
            echo "MODEL_NAME is $MODEL_NAME"
            shift 2
            ;;
        -u|--hf-hub-link)
            HF_REPO_URL="$2"
            git lfs install
            git clone $HF_REPO_URL HF-models/$MODEL_NAME/
            cd HF-models/$MODEL_NAME/
            git lfs install
            git lfs pull
            cd ../..
            touch dummy_file.pth
            torch-model-archiver --model-name $MODEL_NAME --serialized-file dummy_file.pth --version 1.0 --handler scripts/torchserve_vitxxsmall_handler.py --export-path model-store -r requirements.txt
            rm -f dummy_file.pth
            shift 2
            ;;
    esac
done