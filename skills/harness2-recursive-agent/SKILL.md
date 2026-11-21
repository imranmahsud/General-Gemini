---
name: harness2-recursive-agent
description: Recursive AI agent optimization framework by Google Research (Harness²). Optimizes agent prompts, tool definitions, execution trajectories, and memory without fine-tuning model weights.
---

# Harness² Recursive Agent Optimization Guide

## Overview

`Harness²` (`google-research/harness2`) is an open-source research framework that formalizes agent self-improvement. Instead of retraining or fine-tuning weights, it optimizes the surrounding "harness" (system instructions, tool contracts, memory structures, and error-recovery loops) across two recursive levels:
1. **Task-Level Recursion**: Diagnoses failures in the active task to rewrite prompt rules and tool invocations on the fly.
2. **Harness-Level Recursion**: Synthesizes verified patterns and failure modes into persistent skills and instructions for future sessions.

Repository Path: `C:\tools\harness2`

---

## Architecture

- **Rollout Generator**: Executes multiple candidate solution paths in parallel.
- **Trace Inspector**: Evaluates tool call arguments, exit codes, and token budgets.
- **Harness Synthesizer**: Re-weights prompt directives and generates refined schema bindings.

---

## Usage in Agent Workflows

- Run Harness² evaluation sweeps when benchmarking multi-step coding or civil engineering tool pipelines against baseline execution traces.
- Incorporate iterative prompt refinement before committing mission-critical workflows to production.
