# Wiki Schema & Conventions

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
```

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
4. **Log** the sync operation as a single daily entry in `log.md` using the keyword `sync`.
