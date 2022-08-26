

# HF only

## Setup
Log into the terminal of an AWS EC2 `t2.micro` instance with a base AWS Deep Learning PyTorch AMI (as it includes [`torch-model-archiver`](https://github.com/pytorch/serve/tree/master/model-archiver) and `docker`)

The `Using Torchserve Docker containers on EC2 for inference` section of [this Notion blog](https://www.notion.so/Day-2-3-Torchserve-custom-handlers-and-Docker-containers-02665de910a64aedab2b907a9a0cc9b0#3825849dfb8942379df2cdce8a729d9a) by me can be followed for logging into the appropriate AWS EC2 instance.


## Running the Server
Within the AWS EC2 instance, activate the PyTorch environment and navigate to the current folder after cloning this repo: 

```
source activate pytorch
git clone https://github.com/tripathiarpan20/HF-torchserve-pipeline
cd HF-torchserve-pipeline/HF-only
```

Install git-lfs to be able to download 🤗 models from the hub ([reference](https://stackoverflow.com/questions/71448559/git-large-file-storage-how-to-install-git-lfs-on-aws-ec2-linux-2-no-package)):
```
sudo yum install -y amazon-linux-extras
sudo amazon-linux-extras install epel -y
sudo yum-config-manager --enable epel
sudo yum install git-lfs
```

Download the 🤗 model repo with git-lfs ([example](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion/tree/main)) along with all the model dependencies like checkpoints, vocabulary, config etc:
```
git lfs install
mkdir -p model-store/HF-models/
git clone https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion model-store/HF-models/bert_sentiment/
cd model-store/HF-models/bert_sentiment/
git lfs install
git lfs pull
cd ../../..
```

**NOTE**: The cloned repo of the model & the name of the `.mar` file should be exactly the same, this constraint was necessary to register new models with `curl POST` requests flexibly (i.e, during server startup with Docker and after).



Create a Torchserve model archive with the model handler file (`scripts/torchserve_bert_sentiment_handler.py` in our example) along with relevant dependencies in `requirements.txt` (like 🤗 transformers).  

**Note:** Since we are not giving a pretrained checkpoint as a `.pth` file (as it would be downloaded from 🤗 in the `initialize` method of our `torchserve_bert_sentiment_handler.py`), the `--serialized-file` option is redundant and we do not use the context in our handler. 
```
touch dummy_file.pth
torch-model-archiver --model-name bert_sentiment --serialized-file dummy_file.pth --version 1.0 --handler scripts/torchserve_bert_sentiment_handler.py --export-path model-store -r requirements.txt
rm -f dummy_file.pth
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

Run the Torchserve server container with Docker and archived model (refer to [this](https://github.com/pytorch/serve/tree/master/docker#create-torch-model-archiver-from-container) and [this](https://github.com/pytorch/serve/blob/fd4e3e8b72bed67c1e83141265157eed975fec95/docs/use_cases.md#secure-model-serving) for more details):

```
docker run -d --rm -it --shm-size=50g -p 8080:8080 -p 8081:8081 --name torchserve-cpu-prod-bert -v $(pwd)/scripts/config.properties:/home/model-server/config.properties --mount type=bind,source=$(pwd)/model-store,target=/home/model-server/model-store torchserve-cpu-prod torchserve --ncs --model-store=/home/model-server/model-store --ts-config config.properties
```

Check whether the model was started properly (keep trying repeatedly for a few seconds while server boots up):
```
curl http://127.0.0.1:8080/ping
#OR
curl http://127.0.0.1:8081/models/
```

Run for more details:
```
curl http://127.0.0.1:8081/models/bert_sentiment/
```

In case of bugs, can log into the recently created container and check the logs for debugging or metrics(check the [logging documentation](https://github.com/pytorch/serve/blob/master/docs/logging.md) for details)

```
serve_cont_id=$(docker ps -l -q) 
docker exec -it $serve_cont_id /bin/bash
cat logs/model_log.log
```

## Add New models to the Torchserve serve

###TODO  
Hint: 

Modify Hander script to use context and manifest to store HF model name (as in [this]() with `left` and `right`)  
Use `curl POST command` as in [this](https://github.com/pytorch/serve/blob/master/docs/management_api.md#register-a-model)


## Inferencing and Benchmarking

Prepare a sample text
```
echo "This is amazing" > sampleText.txt
```

Send inference requests:
```
curl http://localhost:8080/predictions/bert_sentiment -T sampleText.txt
```