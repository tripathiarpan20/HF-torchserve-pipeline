# HF-ORT

[🤗 Optimum](https://github.com/huggingface/optimum) library allows great inference optimizations that integrate elegantly with the [`pipeline`](https://huggingface.co/docs/transformers/main_classes/pipelines).

References:
* [Quickstart](https://github.com/huggingface/optimum/blob/0ddcb4fbea110577371deb79f4d063fa5aab46a1/README.md#quickstart)
* [Notebook](https://colab.research.google.com/drive/1EQVGxZA0SqX1nBtiZBLeY6LaQtffFYZr?authuser=1#revisionId=0B3_VTcFDUSxZZXorQlBhd1lyM0M1bG5oUkl4aFlyWDBWbUMwPQ)

Several runtime optimzations would be integrated into this repo soon, such as:
- [ONNX runtime inference](https://github.com/huggingface/optimum/blob/0ddcb4fbea110577371deb79f4d063fa5aab46a1/README.md#exporting-transformers-models-to-onnx)
- ONNX static quantized runtime inference
- ONNX dynamic quantized runtime inference