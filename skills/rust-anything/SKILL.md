---
name: rust-anything
description: Incrementally rewrite Python, Node.js, Go, or Java applications in pure Rust with automated verification against recorded production execution traces. Use for migrating slow tools to high-performance compiled Rust.
---

# rust-anything Migration Guide

## Overview

`rust-anything` provides a verified four-phase workflow to migrate slow Python, TypeScript/JavaScript, Go, or Java code into native, memory-safe Rust with zero regression risk:
1. **Record**: Intercepts and logs real execution traces, arguments, edge cases, and return payloads from the existing runtime.
2. **Port**: Generates the Rust crate structure and FFI/C-ABI bridge wrappers.
3. **Check**: Replays the recorded test cases against the compiled Rust binary to assert 100% output parity.
4. **Lift**: Drops the original runtime wrapper, leaving a pure, standalone high-performance Rust executable.

Repository Path: `C:\tools\rust-anything`

---

## Migration Workflow

### 1. Recording Existing Application Traces
```bash
rust-anything record --cmd "python my_slow_script.py input.dat" --cases 50
```

### 2. Generating the Rust Crate Scaffold
```bash
rust-anything port --target ./rust_migrated --lang python
```

### 3. Parity Assertion (Check Step)
```bash
rust-anything check --original "python my_slow_script.py" --candidate "./rust_migrated/target/release/my_fast_app"
```

### 4. Final Standalone Build
```bash
cd ./rust_migrated
cargo build --release
```

---

## Agent Integration Rules

- Use when refactoring high-latency file parsers, GIS geometry converters, or data serialization bottlenecks into compiled binaries.
- Ensure strict regression validation by validating check-diff results before landing code changes.
