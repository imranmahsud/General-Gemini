---
name: openvino-acceleration
description: Hardware-accelerated neural network optimization and inference using Intel OpenVINO on CPU, GPU, and NPU.
---

# OpenVINO Acceleration

Local neural network model quantization, graph optimization, and low-latency inference on Windows and Linux using OpenVINO (`import openvino as ov`).

## Environment & Hardware

- **Python Module**: `openvino` v2026.4.1 (installed in Python 3.12 environment).
- **Available Execution Devices**: `CPU`, `GPU` (DirectX / integrated graphics / discrete GPUs).

## Core Capabilities

1. **Model Optimization**: Convert HuggingFace / PyTorch models to Intermediate Representation (`.xml` + `.bin`) via Model Optimizer / Optimum Intel.
2. **Quantization**: INT8/INT4 weight compression for large models (Whisper, BERT, ResNet, YOLO) allowing smooth execution on low-RAM machines.
3. **Execution Pipeline**:
```python
import openvino as ov

core = ov.Core()
print("Available Devices:", core.available_devices)

# Load and compile model for best device
# model = core.read_model("model.xml")
# compiled_model = core.compile_model(model, device_name="AUTO")
```
