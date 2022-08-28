# HF-ORT

[🤗 Optimum](https://github.com/huggingface/optimum) library allows great inference optimizations that integrate elegantly with the [`pipeline`](https://huggingface.co/docs/transformers/main_classes/pipelines).

Several runtime optimzations would be integrated into this repo soon, such as:
- [ONNX runtime inference](https://github.com/huggingface/optimum/blob/0ddcb4fbea110577371deb79f4d063fa5aab46a1/README.md#exporting-transformers-models-to-onnx)
- ONNX static quantized runtime inference
- ONNX dynamic quantized runtime inference