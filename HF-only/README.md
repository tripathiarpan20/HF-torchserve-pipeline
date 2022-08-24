

# HF only

## Setup
Log into the terminal of an AWS EC2 `t2.micro` instance with a base AWS Deep Learning PyTorch AMI (as it includes [`torch-model-archiver`](https://github.com/pytorch/serve/tree/master/model-archiver) and `docker`)

The `Using Torchserve Docker containers on EC2 for inference` section of [this Notion blog](https://www.notion.so/Day-2-3-Torchserve-custom-handlers-and-Docker-containers-02665de910a64aedab2b907a9a0cc9b0#3825849dfb8942379df2cdce8a729d9a) by me can be followed for logging into the appropriate AWS EC2 instance.


## Running the Server
Within the AWS EC2 instance, activate the PyTorch environment and navigate to the current folder after cloning this repo: 

```
conda activate pytorch
git clone https://github.com/tripathiarpan20/HF-torchserve-pipeline
cd HF-torchserve-pipeline/HF-only
```

Create a Torchserve model archive along with relevant dependencies in `requirements.txt` (like 🤗 transformers).  

**Note:** Since we are not giving a pretrained checkpoint as a `.pth` file (as it would be downloaded from 🤗 in the `initialize` method of our `torchserve_bert_sentiment_handler.py`), the `--serialized-file` option is redundant and we do not use the context in our handler. 
```
mkdir -p model-store
touch dummy_file.pth
torch-model-archiver --model-name bert_sentiment --serialized-file dummy_file.pth --version 1.0 --handler scripts/torchserve_bert_sentiment_handler.py --export-path model-store -r requirements.txt
rm dummy_file.pth
```


Build a Torchserve CPU Docker container:
```
git clone https://github.com/pytorch/serve.git
cd serve/docker
./build_image.sh -bt production -t torchserve-cpu-prod
cd ../..
rm -rf serve
```

Check whether the Torchserve container is present in the list of Docker images:
```
docker images
```

Run the Torchserve server with Docker and archived model (refer to [this](https://github.com/pytorch/serve/tree/master/docker#create-torch-model-archiver-from-container) and [this](https://github.com/pytorch/serve/blob/fd4e3e8b72bed67c1e83141265157eed975fec95/docs/use_cases.md#secure-model-serving) for more details):

```
docker run -d --rm -it -p 8080:8080 -p 8081:8081 --name torchserve-cpu-prod-bert -v $(pwd)/model-store:/home/model-server/model-store -v $(pwd)/scripts/config.properties:/home/model-server/config.properties torchserve-cpu-prod torchserve --ncs --model-store=/home/model-server/model-store --ts-config config.properties
```

## Inferencing and Benchmarking