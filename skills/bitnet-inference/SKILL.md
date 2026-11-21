---
name: bitnet-inference
description: Run 1-bit quantized LLMs (BitNet b1.58) on CPU with high throughput and minimal memory footprint using Microsoft bitnet.cpp. Use when running large models without a dedicated GPU or when deploying local CPU-only AI inference.
---

# bitnet.cpp CPU Inference Guide

## Overview

`bitnet.cpp` is Microsoft's official inference framework for 1-bit Large Language Models (specifically `BitNet b1.58`). It replaces floating-point matrix multiplications with ternary additions and subtractions (weights restricted to $\{-1, 0, 1\}$), achieving up to 4x energy efficiency and multi-token-per-second throughput on standard x86 and ARM CPUs without requiring GPU VRAM.

Repository Path: `C:\tools\bitnet`

---

## Architecture & Capabilities

1. **Native CPU Kernels**: Hand-tuned SIMD AVX2, AVX-512, and ARM NEON kernels.
2. **Zero VRAM Footprint**: A 100B parameter BitNet model runs within ~12–15 GB of standard host RAM on CPU.
3. **Hardware Compatibility**: Runs directly on modern multi-core CPUs (AMD Ryzen, Intel Core) without CUDA or ROCm dependencies.

---

## Build & Setup on Windows

### 1. Prerequisites
- CMake 3.22+
- Python 3.10+
- Clang / MSVC C++ Build Tools

### 2. Compilation
```powershell
cd C:\tools\bitnet
python -m pip install -r requirements.txt
python setup_env.py --compiler cl
```

### 3. Running Model Inference
```powershell
# Run inference with BitNet b1.58 3B / 7B / 100B
python run_inference.py -m models/bitnet_b1_58-large -p "Summarize structural load transfer:" -n 128 --temp 0.2
```

---

## Workflow Integration

- Use `bitnet.cpp` when deploying background agent reasoning tasks on laptops or headless CPU mini-servers (e.g. Lenovo ThinkCentre Tiny) where 0 MB GPU VRAM is available.
- Combine with `qwen.bat` or local Ollama instances for lightweight hybrid orchestration.
