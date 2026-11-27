---
name: elephant-goldfish-architecture
description: Dual-session context architecture for AI agent workflows based on Google Research (EGM). Separates long-term architectural vision (Elephant) from zero-context, objective verification subagents (Goldfish).
---

# Elephant-Goldfish Model (EGM) Architecture

## Overview

The Elephant-Goldfish Model solves context pollution and agent confirmation bias in extended engineering sessions:
1. **The Elephant (Deep Context)**: The primary coordinator session that retains the full project history, ADRs, business logic, and architectural vision. It drafts design specifications and contracts.
2. **The Goldfish (Zero Context)**: Fresh, ephemeral subagents spawned with strictly zero conversation history. They are given only the specification and the filesystem to review and execute without preconceptions or historical bias.

Repository Path: `C:\tools\elephant-goldfish-model`

---

## Operating Protocol

1. **Phase 1: Elephant Specification**: Coordinator documents scope and requirements into an unambiguous specification file (`SPEC.md`).
2. **Phase 2: Goldfish Verification**: Coordinator invokes a fresh subagent with role "Cold Reviewer" to audit the spec against the codebase without prior chat memory.
3. **Phase 3: Execution & Gate Check**: Independent Goldfish subagents implement modular slices, reporting clean completion signals back to the Elephant coordinator.
