---
name: agent-client-protocol
description: Open standard protocol (ACP) connecting code editors, IDEs, and desktop shells to AI coding agents via standard JSON-RPC over stdio. Complementary to Model Context Protocol (MCP).
---

# Agent Client Protocol (ACP) Guide

## Overview

The `Agent Client Protocol` (`agentclientprotocol/agent-client-protocol`) is an open standard designed to decouple coding agents from specific editors. While MCP standardizes how agents talk to tools and data sources, ACP standardizes how agents communicate with user interfaces (Zed, VS Code, Neovim, terminal shells).

Repository Path: `C:\tools\agent-client-protocol`

---

## Core Specification

1. **Transport**: JSON-RPC 2.0 over `stdio`.
2. **Capabilities**:
   - `session/init`: Handshake and protocol version negotiation.
   - `fs/edit`: Editor-assisted atomic diffs and syntax-aware patching.
   - `diagnostics/report`: Live compilation/linter feedback delivered directly into agent context.
   - `terminal/spawn`: Safe sandboxed terminal sessions managed by the host IDE.
