# HF-torchserver-scripted
 
This repository contains an example to deploy models with third-party dependencies (like 🤗 Transformers, sparseml etc) on Torchserve servers as ready-for-usage Docker containers on cloud services like AWS.  

For the context of this repository, we would deploy the models on an AWS [`t2.micro`](https://aws.amazon.com/ec2/instance-types/) instance which can be used for free (for 750 hours) on a new AWS account. We work with a 🤗 BERT Transformer [model](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion) for the task of sentiment analysis by using its [`pipeline`](https://huggingface.co/docs/transformers/main_classes/pipelines) feature, the handler code in `scripts` can also be used as a simplistic template to deploy an 🤗 `pipeline`.

We would also benchmark the REST API calls in time units and compare the model performances for the following approaches: 
* Deploying the [DistilBERT](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion) Huggingface model with a custom torchserve handler.
* Deploying the [DistilBERT](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion) Huggingface model in [scripted mode](https://pytorch.org/tutorials/beginner/Intro_to_TorchScript_tutorial.html) with a custom torchserve handler.


## TODO
- [ ] Add Torchscripted model
- [ ] Add multi-GPU inferencing explanation