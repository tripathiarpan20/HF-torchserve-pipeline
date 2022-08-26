# HF-torchserve-pipeline
 
This repository contains an example to deploy models with third-party dependencies (like 🤗 Transformers, sparseml etc) on Torchserve servers as ready-for-usage Docker containers on cloud services like AWS.  

For the context of this repository, we would deploy the models on an AWS [`t2.micro`](https://aws.amazon.com/ec2/instance-types/) instance which can be used for free (for 750 hours) on a new AWS account. We work with a 🤗 BERT Transformer [model](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion) for the task of sentiment analysis by using its [`pipeline`](https://huggingface.co/docs/transformers/main_classes/pipelines) feature, the handler code in `scripts` can also be used as a simplistic template to deploy an 🤗 `pipeline`.

This work *may* also be extended to deploy the Torchserve Docker containers with HF models at scale with [AWS Cloudformation](https://github.com/pytorch/serve/tree/master/examples/cloudformation) & [AWS EKS](https://github.com/pytorch/serve/tree/master/kubernetes/EKS) as explained in the official Torchserve repo & [AWS Sagemaker](https://github.com/tescal2/TorchServeOnAWS/tree/master/3_torchserve_byoc_with_amazon_sagemaker), incorporating utilities like AWS ELB & Cloudwatch.

We would also benchmark the REST API calls in time units and compare the model performances for the following approaches: 
* Deploying the [DistilBERT](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion) Huggingface model with a custom torchserve handler. (refer `HF-only` directory)
* Deploying the [DistilBERT](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion) Huggingface model in [scripted mode](https://pytorch.org/tutorials/beginner/Intro_to_TorchScript_tutorial.html) with a custom torchserve handler. (refer `HF-scripted` directory)


## Todo
- [ ] Verify HF pipeline functionality with  AWS EC2 `t2.micro`
- [ ] Add [AB Testing](https://github.com/pytorch/serve/tree/master/benchmarks) experiments with Torchserve Benchmarking utilities.
- [ ] Add dynamic batching explanation
- [ ] Add Torchscripted model code
- [ ] Add inference optimizations from [🤗 optimum](https://github.com/huggingface/optimum) library.
- [ ] Try [LLM.int8](https://twitter.com/Tim_Dettmers/status/1559892888326049792) integration


## References
* [My Torchserve + AWS Notion journal](https://garrulous-saxophone-8a6.notion.site/AWS-Torchserve-resources-52fdfd81fa1c4a5ebb9a5fd7398ed552)
* https://github.com/pytorch/serve
* https://huggingface.co/docs/transformers/main_classes/pipelines
* https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion
* https://huggingface.co/course/chapter2/2?fw=pt
* https://huggingface.co/docs/transformers/main_classes/pipelines
* https://github.com/aws-samples/amazon-sagemaker-endpoint-deployment-of-siamese-network-with-torchserve
* https://github.com/cceyda/lit-NER
* https://github.com/tescal2/TorchServeOnAWS
* https://huggingface.co/spaces/lewtun/twitter-sentiments

## Support
There are many ways to support an open-source work, ⭐ing it is one of them. 

## Issues
In case of bugs or queries, raise an Issue, or even better, raise a PR with fixes.