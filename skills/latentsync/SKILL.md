---
name: latentsync
description: End-to-end audio-conditioned lip-synchronization using ByteDance LatentSync latent diffusion models. Synchronizes facial video movements with arbitrary voice/speech audio tracks with temporal consistency and zero intermediate 3D face meshes.
---

# LatentSync (Audio-Conditioned Lip Synchronization)

LatentSync is ByteDance's latent diffusion lip-synchronization framework. It maps speech audio directly to video frames in latent space using cross-attention Whisper embeddings and Stable Diffusion U-Nets.

- **Local Repository**: `C:\tools\LatentSync`
- **GitHub**: `https://github.com/bytedance/LatentSync`
- **HuggingFace Weights**: `ByteDance/LatentSync-1.6`

## Hardware & Environment Requirements
- **VRAM Requirements**:
  - LatentSync 1.5 (256x256): >= 8 GB VRAM.
  - LatentSync 1.6 (512x512): >= 18 GB VRAM (or DeepCache enabled).
- **Core Dependencies**: Python 3.10/3.11, PyTorch (CUDA), FFmpeg.

## CLI Execution Pattern

Run inference using the modular script:

```bash
python -m scripts.inference \
    --unet_config_path "configs/unet/stage2_512.yaml" \
    --inference_ckpt_path "checkpoints/latentsync_unet.pt" \
    --inference_steps 25 \
    --guidance_scale 1.5 \
    --enable_deepcache \
    --video_path "input_avatar.mp4" \
    --audio_path "speech.wav" \
    --video_out_path "synced_output.mp4"
```

## Parameter Optimization
- **`--inference_steps`** `[20-50]`: Higher values (e.g. 30-40) increase edge sharpness around the mouth; lower values (20) accelerate render speeds.
- **`--guidance_scale`** `[1.0-2.5]`: Controls audio synchrony constraint. 1.5 is optimal balance. Above 2.5 can introduce temporal warping around the jawline.
- **`--enable_deepcache`**: Skips redundant U-Net layer evaluations between frames for ~2x faster rendering.

## Pipeline Integration
Use in tandem with `speech-to-text` (ElevenLabs / Whisper) or `text-to-speech` to synthesize full talking-head segments from raw scripts.
