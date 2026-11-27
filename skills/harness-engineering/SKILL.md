---
name: harness-engineering
description: Harness engineering best practices, architectures, benchmark suites, and recursive agent evaluation based on walkinglabs/awesome-harness-engineering and Google Research Harness2.
---

# Harness Engineering & Evaluation Guide

## Core Architecture
Harness engineering focuses on building robust execution environments, benchmark sandboxes, and verification loops for autonomous agents.

### Key Pillars
1. **Deterministic Testbeds**: Mocking tool environments and operating systems to evaluate multi-turn tasks repeatably.
2. **Substrate Separation**: Distinguishing the orchestration layer (agent controller) from the execution substrate (sandboxed terminal, browser, or API runner).
3. **Multi-Agent Evaluation**: Measuring convergence, tool selection efficiency, context compaction, and failure recovery.
4. **Local Benchmarks**: Using Google Research `harness2` (`jb` JobBench, `lab` WebBench, `wb` WorkBuddy) for zero-token-leakage offline evaluations.

## Local Reference & Tools
- Knowledgebase: `C:\tools\awesome-harness-engineering`
- Runner: `C:\tools\harness2\scripts\check_setup.py`
