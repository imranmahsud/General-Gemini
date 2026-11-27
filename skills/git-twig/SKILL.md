---
name: git-twig
description: Lightweight git worktree management for AI coding agents. Creates isolated sibling checkouts with up to 97% disk savings using Copy-on-Write (CoW). Use when dispatching subagents, testing parallel features, or running isolated git worktrees.
---

# git-twig (Lightweight Git Worktrees for AI Agents)

`git-twig` manages lightweight, fast, Copy-on-Write (CoW) git worktrees tailored for parallel coding agents and background tasks without cloning duplicate repository storage.

- **Local Repository**: `C:\tools\git-twig`
- **GitHub**: `https://github.com/leostera/git-twig`

## Why Use Twig for Agents

When spinning up subagents or parallel tasks:
- Standard full clones (`git clone`) duplicate the `.git` directory, taking gigabytes of disk and excessive I/O.
- Standard `git worktree` creates full checkouts of committed files.
- `git twig` leverages filesystem Copy-on-Write (Windows Dev Drive / ReFS, Linux Btrfs/XFS, macOS APFS) to link matching files across sibling worktrees, reducing disk usage by up to 97%.

## Command Reference

### 1. Create a Worktree for a Subagent
Always place sibling agent worktrees beside the primary repository rather than nested inside it:

```bash
# Create a new branch and lightweight worktree
git -C <repo-path> twig new -b <branch-name> <sibling-path> HEAD

# Example:
git -C "C:\Users\Imran\project" twig new -b feat/agent-1 "C:\Users\Imran\project-agent-1" HEAD
```

### 2. List Active Twig Worktrees
```bash
git -C <repo-path> twig list
```

### 3. Adopt Existing Worktrees into Twig
Reorganize and consolidate external worktrees:
```bash
git twig adopt --dry-run --worktrees-dir=<worktrees-dir>
git twig adopt --worktrees-dir=<worktrees-dir>
```

### 4. Remove / Cleanup Worktrees
Always verify the agent's work has been committed or integrated before removal:
```bash
git -C <repo-path> worktree remove <worktree-path>
```

## Agent Guidelines
1. **Sibling Checkouts**: Always place agent checkouts beside the source repository (`../feature-branch`), never nested.
2. **Fast-forward Integration**: Merge coherent, tested increments promptly into main; local branches in worktrees are staging grounds, not permanent archives.
3. **No Hardlinks to Source**: Writes inside twigs are private and never corrupt the parent checkout.
