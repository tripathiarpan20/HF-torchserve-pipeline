'''
References: 
(i) https://github.com/pytorch/serve/blob/master/docs/custom_service.md
(ii) https://github.com/pytorch/serve/blob/master/ts/torch_handler/base_handler.py 
(iii) https://github.com/pytorch/serve/blob/master/ts/torch_handler/text_handler.py
(iv) https://github.com/cceyda/lit-NER/blob/master/lit_ner/serve_pretrained.py

Reference that implements handler class without inheriting the `BaseHandler`:
(i) https://github.com/aws-samples/amazon-sagemaker-endpoint-deployment-of-siamese-network-with-torchserve/blob/main/deployment/handler.py 


Batching 🤗 model & Torchserve inputs in the handler: https://youtu.be/M6adb1j2jPI
https://github.com/pytorch/serve/issues/1783

'''

import torch
from ts.torch_handler.base_handler import BaseHandler
from transformers import pipeline



class DistilBERTEmotionHandler(BaseHandler):
    def __init__(self):
        super().__init__(self)
        self.tokenizer = None

    def load_model(self):
        pipe = pipeline(task="sentiment-analysis", model="bhadresh-savani/distilbert-base-uncased-emotion")
        return pipe

    def initialize(self, context):


        '''
        context.system_properties['gpu_id'] is decided by Torchserve server to utilize 
        all available GPUs for inference equally:
        https://github.com/pytorch/serve/blob/master/docs/custom_service.md#handling-model-execution-on-multiple-gpus
        '''
        properties = context.system_properties
        self.map_location = (
            "cuda"
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else "cpu"
        )
        self.device = torch.device(
            self.map_location + ":" + str(properties.get("gpu_id"))
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else self.map_location
        )
        self.manifest = context.manifest


        #Loading model on the 'device' decided by Torchserve
        #----------------------------------------
        self.initialized = False

        self.model = self.load_model()
        self.model.model.to(self.device)

        self.initialized = True
        #----------------------------------------

    def preprocess(self, data):
        '''
        Need to write code to convert the input batch into List[str] that can be processed by the `pipeline` as in this example:
        https://huggingface.co/spaces/lewtun/twitter-sentiments/blob/main/app.py#L34
        '''
        return data

    def inference(self, data):
        preds = self.model(data)

        response = dict()
        response["labels"] = [pred["label"] for pred in preds]
        response["scores"] = [pred["score"] for pred in preds]
        return response

    def postprocess(self, data):
        return data.tolist()

    
    '''
    The `handle` function can also be overrided if we want to support multiple inputs for each Inference requests, for example,
    `left` and `right` inputs supported in this project: https://github.com/aws-samples/amazon-sagemaker-endpoint-deployment-of-siamese-network-with-torchserve#torchserve-in-action

    Multiple outputs can also be returned as in this example:
    https://github.com/pytorch/serve/issues/1647
    '''
