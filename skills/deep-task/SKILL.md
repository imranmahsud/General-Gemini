---
name: deep-task
description: Deconstruct and deepen complex user instructions into senior principal engineering standards using Felix Rieseberg's 4-pillar deep-task framework. Use when the user requests a deep breakdown, wants to elevate a task beyond surface-level summaries, or uses "deepen this task".
---

# Deep Task (Felix Rieseberg Framework)

This skill deepens technical tasks rather than simply expanding word count or adding fluff. It enforces the 4-pillar inquiry framework developed by senior engineering leadership at Anthropic.

---

## 4-Pillar Deepening Protocol

When executing or rewriting any technical task under this framework, execute these four evaluations in sequence before taking action:

### Pillar 1: Professional Delta
- **Question**: What would a senior principal engineer or domain master in this field do that the prompt has not explicitly asked for?
- **Action**: Identify edge cases, architectural failure modes, concurrency issues, production-hardening steps, and domain-specific best practices.

### Pillar 2: Ground-Truth Raw Material
- **Question**: What is the rawest source material to start from, rather than pre-digested summaries or third-party interpretations?
- **Action**: Bypass high-level blog posts or secondary wrappers. Directly target primary source code, RFC specifications, raw sensor/telemetry data, official API schemas, or low-level binary artifacts.

### Pillar 3: Professional Toolchain & Methodology
- **Question**: What specific industry-standard tools, profilers, compilers, or mathematical methods would top practitioners deploy?
- **Action**: Replace generic scripts or manual inspection with established toolchains (e.g., Ghidra for reverse engineering, HEC-RAS/QGIS for hydraulics, PyTest/GoogleTest for verification, Perf/VTune for profiling).

### Pillar 4: Objective Non-AI Verification Gate
- **Question**: What external verification (independent of LLM opinion) proves the solution is correct?
- **Action**: Define deterministic checks: exit code 0 on test runners, static analysis passing, memory leak sanitizers (ASan/Valgrind) clean, mathematical boundary invariants satisfied, or automated schema validation.

---

## Execution Workflow

1. State the **Professional Delta** (what top experts do that was unsaid).
2. Specify the **Rawest Material** (the ground-truth starting point).
3. Select the **Specific Tools & Methods** (the definitive practitioner stack).
4. Define the **Objective Verification Gate** (the automated truth test).
5. Output the **Rewritten Deep Prompt & Execution Plan**.
