---
tags: [project, meta, schema, maintenance]
created: 2026-06-18
updated: 2026-06-18
status: "🟢 Completed"
description: "Documentation and prompt templates for the weekly deterministic (Script) and strategic (Agent) wiki sync system."
sources: ["[[schema]]"]
---

# Project: Wiki Sync Plan & Runbook

This note defines the workflow, script details, and agent instructions for the weekly Nexus wiki sync system. It combines **Option C (Deterministic Script Sync)** and **Option A (Strategic Agent Sync)** to ensure that micro-updates to individual notes propagate cleanly to macro-level dashboards and playbooks.

---

## 1. Option C: Deterministic Script Sync (Syntactic Bookkeeping)

The local Python script at `scripts/sync.py` automates the structural bookkeeping of the workspace.

### What it does:
1. **Rebuilds index.md**: Scans `notes/`, `projects/`, and `sources/` directories. For each note, it extracts the H1 display title, the frontmatter `updated` date, and the frontmatter `description` (reusing any manually-written descriptions currently in the index if the note lacks a frontmatter description). It then rewrites [index.md](file:///Users/kimjiwoo/Documents/coding/nexus/index.md), sorting entries in descending order of updated date.
2. **Updates Deliverables Status**: Automatically scans all project trackers in `projects/` for any table under a `## Deliverables Status Dashboard` (or `## Deliverables Dashboard`) header. It reads the `status` YAML property from the linked notes and writes it directly back to the Status column of that table.

### How to run it:
Open your terminal inside the workspace root and run:
```bash
python3 scripts/sync.py
```

---

## 2. Option A: Strategic Agent Sync (Semantic Synthesis)

When you make updates that change the *meaning* or *strategy* of your notes, you can ask the AI agent to run a strategic sync.

### Prompt to copy/paste:
Copy and paste the prompt below into the chat when you want to run a weekly strategic sync:

```markdown
Let's run the weekly strategic sync for this workspace. Please follow these steps:
1. Read the list of files modified recently (you can check file mtimes or the `updated` frontmatter dates).
2. Analyze the changes in those notes to understand any semantic shifts (e.g., shifts in project roadmaps, new evidence, or updated concepts).
3. Propagate these shifts to the master files (such as main roadmaps or evidence logs if they exist).
4. Scan the workspace for any contradictions or gaps introduced by the updates and report them.
5. Record this operation as a single consolidated entry in [[log]] for today's date using the keyword `sync` or `maintenance`.
```

---

## 3. Metadata Standards (Conventions)

For the sync system to operate correctly, keep notes updated with these frontmatter properties:

```yaml
---
status: "🟢 Completed"  # Use for files tracked in deliverables dashboards
description: "Brief one-line summary of this file's contents"
updated: YYYY-MM-DD    # Always update this date when editing a file
---
```

### Valid Status Values (Recommended):
* `🔴 Planned`
* `🟡 In Progress`
* `🟢 Completed`
