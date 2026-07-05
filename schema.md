# Nexus Schema & Conventions

This file defines the directory structure, formatting rules, and maintenance workflows for the Nexus workspace.

---

## 1. Directory Structure

```
├── schema.md          # this file — conventions & workflows
├── AGENTS.md          # AI instructions constitution
├── index.md           # content catalog (by category)
├── log.md             # chronological operations log
├── assets/            # static assets, images, and media
├── sources/           # one summary page per ingested source (immutable)
├── projects/          # plans and trackers
└── notes/             # synthesized notes on entities, concepts, and analyses

.claude/skills/        # agent capability layer (self-improvement) — outside content; see §4
```

> **Access:** The Nexus content folders and root markdown files are writable. The one writable location *outside* content is `.claude/skills/` (capabilities, not knowledge). Everything else is read-only.

---

## 2. Page Conventions

### Naming Convention
- **Files:** `lowercase-with-hyphens.md` (e.g., `vector-search.md`, `context-decay.md`).
- **Wikilinks:** Use Obsidian-style wikilinks: `[[Page Name]]` (or `[[folder/page-name|Page Name]]` for nested paths).

### Frontmatter (YAML)
Every markdown page must include:
```yaml
---
tags: [relevant, tags]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["[[source page]]"]
---
```

### Style Criteria
- **First principles.** Analyze topics from fundamental truths.
- **Brief & concise.** Avoid wordy filler. Focus on dense, structured notes.
- Use lists and tables over large walls of prose.

---

## 3. Core Workflows

### Ingest Workflow
1. **Read** the raw input draft or log.
2. **Create** `sources/<source-name>.md` to store the raw summary.
3. **Update or Create** connected notes in `notes/`.
4. **Link** files together using bi-directional Wikilinks.
5. **Update** `index.md` and log the change in `log.md`.

### Lint Workflow
1. **Scan** files for orphaned nodes (pages with no incoming links) or missing references.
2. **Standardize** broken link layouts.
3. **Format** headings and list elements.

### Sync Workflow
1. **Run** local sync script (`python3 scripts/sync.py`) to rebuild index lists and propagate `status` metadata.
2. **Review** files modified in the past week to extract semantic/strategic updates.
3. **Propagate** changes to master roadmaps or evidence logs.
4. **Consolidate** the learning loop: collect all `Lessons:` lines logged since the last sync; promote recurring patterns into a skill or a schema amendment, refine skills that misfired, and prune skills that never fire (see `AGENTS.md` Golden Rule 6).
5. **Log** the sync operation as a single daily entry in `log.md` using the keyword `sync` (plus `skill` sub-bullets if skills changed).

### Reflect Workflow
Automatic — the closing step of every non-trivial operation (Ingest, Lint, Sync, or maintenance). Not a separate session; it happens inside the operation that just ran.
1. **Ask** briefly: did anything mislead, surprise, or repeat? Was any instruction in the schema or `AGENTS.md` wrong or missing? Did a reusable multi-step procedure emerge?
2. **Record** the answer as a single `- Lessons:` line in the day's `log.md` entry. No lesson → no line; never force one.
3. **Act immediately** only when the lesson is sharp: fix a wrong schema claim on the spot, or create/refine a skill. Everything else waits for Sync consolidation.

### Self-Improvement Workflow (Skills)
The agent's reusable *capabilities* live in `.claude/skills/`, separate from the *knowledge* in `notes/`/`sources/`. The loop is **closed** — *Execute → Reflect → Consolidate* (see `AGENTS.md` Golden Rule 6).
1. **Create** a skill autonomously when a task surfaces a clearly reusable multi-step procedure (announce it to the user when you do), or when Sync consolidation promotes a recurring `Lessons:` pattern.
2. **Structure:** a skill folder containing `SKILL.md` with `name` + `description` frontmatter capturing the repeatable procedure.
3. **Refine** an existing skill's `SKILL.md` when it underperforms in use, rather than spawning a near-duplicate.
4. **Log** the operation as a single daily entry in `log.md` using the keyword `skill`. Keep skills few — each `description` permanently occupies agent context.
