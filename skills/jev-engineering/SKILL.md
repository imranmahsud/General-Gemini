---
name: jev-engineering
description: Jev System One decision harness for coding agents based on Diogo Almeida (TypeSafe AI / InstructGPT co-author). Cuts token latency up to 200x and costs up to 400x using five typed state notes instead of conversational prose.
---

# Jev Engineering Harness for Coding Agents

## Core Principles
1. **Machine-Native Communication**: Replace free-form prose and conversational chat between internal agent loops with 5 compact typed decisions.
2. **Tyranny of the KV Cache Elimination**: Never send massive conversational histories back and forth for simple routing, classification, or tool choices.
3. **Single Code Station**: Only one dedicated station executes or writes code; all other stations output discrete routing signals.

## The 5 Typed Decision Primitives
Every task cycle is mediated by 5 typed notes:
1. `TASK`: Target specification & acceptance criteria (immutable contract).
2. `STATE`: Current workspace condition (files modified, test pass/fail bit).
3. `ROUTE`: Discrete tool selection / next action index (enum/categorical).
4. `BOUNDS`: Constraints (timeout, memory, allowed directories, rate limits).
5. `VERDICT`: Binary pass/fail validation check.

## Operational Workflow
- **Preflight**: Verify task bounds against workspace trust.
- **Station 1 (Router)**: Select action without generating prose.
- **Station 2 (Implementer)**: Focused code generation inside target scope only.
- **Station 3 (Verifier)**: Automated lint/test run returning boolean state.
