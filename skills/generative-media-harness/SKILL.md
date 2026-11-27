---
name: generative-media-harness
description: Inference and pipeline guidelines for Alibaba Wan 2.1/2.2 video generation, Lightricks LTX-Video, and Tongyi Z-Image-Turbo.
---

# Generative Video & Image Harness

Local and cloud workflows for state-of-the-art open-weights video and image models stored in `C:\tools\`.

## Installed Repositories

1. **`Wan-Video` (`C:\tools\Wan-Video`)**:
   - Alibaba open-source video generative model family (Wan2.1 / Wan2.2).
   - Text-to-Video and Image-to-Video with high cinematic quality and text rendering.
   - Script: `C:\tools\Wan-Video\generate.py`.
2. **`LTX-Video` (`C:\tools\LTX-Video`)**:
   - Lightricks DiT video foundation model.
   - Optimized for fast, low-latency video generation and real-time generation loops.
3. **`Z-Image` (`C:\tools\Z-Image`)**:
   - Tongyi-MAI 6B-parameter distilled diffusion model.
   - Ultra-fast 8-step image synthesis with bilingual text rendering.
   - Script: `C:\tools\Z-Image\inference.py`.

## GPU Requirements & Execution Notice

- **Hardware Note**: High-resolution video generation (Wan 2.1/2.2) and large image diffusion models require dedicated high-VRAM GPUs (16GB+ VRAM, CUDA/DirectX).
- On systems with integrated graphics (AMD Radeon 1GB VRAM), execute via OpenVINO INT8 CPU pipelines, cloud APIs (e.g. FAL.ai, Replicate, HuggingFace Inference Endpoints), or low-resolution distilled runs.
