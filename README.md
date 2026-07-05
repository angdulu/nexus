# Nexus: Stateful Cognitive Infrastructure Template

A clean, open-source starter template for building a **Stateful Second Brain** using Obsidian, structured Markdown schemas, and CouchDB synchronization. This system transitions LLM interactions from stateless, ephemeral chat sessions into a compounding, persistent knowledge base.

---

## Core Philosophy

Standard Retrieval-Augmented Generation (RAG) is stateless—the AI agent starts fresh on every session, losing context over long intervals. The **Nexus Pattern** shifts this dynamic by giving the AI read and write access to a local, structured directory of markdown notes governed by a strict "constitution." 

Every session's code files, research briefs, and daily notes are parsed, cross-referenced, and compiled back into the database by the AI.

Beyond storing knowledge, Nexus is **self-updating**: the maintainer agent reflects on every operation, records what it learned, and revises its own procedures and rules over time. It runs a closed growth loop — **Execute → Reflect → Consolidate** — so the system compounds on two axes at once: the *knowledge* it holds, and the *capabilities and conventions* it uses to maintain that knowledge (see "The Self-Updating Loop" below).

---

## Directory Structure

This template contains the following standard folder architecture for clean separation of concerns:

```
nexus/
├── schema.md          # System constitution (rules & conventions)
├── AGENTS.md          # Prompt guide/permissions for agent models
├── index.md           # Central hub cataloging all nodes
├── log.md             # Consolidated chronological operations log
├── scripts/           # Maintenance scripts (sync.py)
├── assets/            # Graphs, diagrams, and static assets
├── sources/           # Summarized logs of raw ingest data (read-only)
├── projects/          # Multi-step execution plans and trackers
└── notes/             # Synthesized profiles on entities, concepts, and analyses

.claude/skills/        # Agent capability layer (self-improvement) — capabilities, not knowledge
```

---

## Schema Conventions

To preserve readability and ensure that AI models do not pollute the database, all files must adhere to standard rules defined in `schema.md`:

1. **File Names:** Lowercase-with-hyphens (e.g. `muscle-memory-model.md`).
2. **YAML Frontmatter:** Every node must maintain a unified header:
   ```yaml
   ---
   tags: [tag1, tag2]
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   sources: ["[[source-note-link]]"]
   ---
   ```
3. **Bi-directional Links:** Cross-references must use standard Obsidian Wikilinks: `[[Node Name]]`.

---

## Setup Guide

### 1. Initialize Obsidian Workspace
Clone this repository or copy the folder structure to your local drive. Open the directory as a vault inside [Obsidian](https://obsidian.md).

### 2. Configure Your AI Environment
When using coding agents (such as Antigravity, Claude Code, or custom API wrappers), place the `AGENTS.md` system prompt inside the root directory. This acts as a sandbox boundary, directing the agent to write updates only into the note directories designated in `schema.md` (e.g. `notes/`, `sources/`, `projects/`) while enforcing schema rules.

### 3. Local Chunk-Level Synchronization (CouchDB)
To sync your markdown notes across devices securely and offline, use the CouchDB database sync configuration:
1. Spin up a local CouchDB Docker container:
   ```bash
   docker run -d -p 5984:5984 --name obsidian-couchdb couchdb
   ```
2. Configure a sync plugin (such as Obsidian Self-Hosted LiveSync) to connect to `http://localhost:5984/nexus`.
3. Map your `/etc/hosts` or local network to enable peer-to-peer replication between your phone and laptop.

---

## Maintenance: The Weekly Sync

Wikis rot when the bookkeeping grows faster than the value. Nexus keeps that in check with a weekly two-stage sync that separates mechanical work from judgment work.

### Stage 1 — Deterministic Script (syntactic bookkeeping)

Run the local Python script to rebuild structural metadata. It makes no model calls:

```bash
python3 scripts/sync.py
```

It will:
- **Rebuild `index.md`** by scanning `projects/`, `sources/`, and `notes/`, pulling each file's H1 title, `updated` date, and `description` (reusing the existing index description where a note has none), then re-sorting every section by most-recently-updated.
- **Propagate status** into project trackers by reading the `status` frontmatter of linked notes and writing it back into any "Deliverables" table.

### Stage 2 — Strategic Agent (semantic synthesis)

When edits change the *meaning* of your notes rather than just their metadata, ask your AI agent to run a strategic pass. It should:
1. Read the files modified in the past week (via `updated` dates or file mtimes).
2. Propagate meaning-level shifts into your master synthesis notes.
3. Report any contradictions or gaps the week's changes introduced.
4. **Consolidate the learning loop:** collect every `Lessons:` line logged since the last sync, promote recurring patterns into a skill or a `schema.md` amendment, refine skills that misfired, and prune skills that never fired (see "The Self-Updating Loop" below).
5. Log the operation as a single dated entry in `log.md` using the keyword `sync` (plus `skill` sub-bullets if skills changed).

The split keeps cheap, mechanical work fully deterministic while reserving the model for the judgment calls.

---

## The Self-Updating Loop (Reflect → Skills → Consolidate)

A plain knowledge base remembers *facts*. Nexus adds a second, separate memory for *capabilities* — the agent's growing toolkit of repeatable procedures — in `.claude/skills/`, and a reflection habit that lets the agent revise its own rules.

The knowledge/capability distinction is strict and load-bearing:

| Layer | Lives in | Holds |
| :--- | :--- | :--- |
| **Knowledge** | `notes/`, `sources/` | What you know |
| **Capability** | `.claude/skills/` | How the agent works |

### 1. Reflect (the closing step of every operation)

Reflection is not a separate session — it happens *inside* every non-trivial operation (Ingest, Lint, Sync, maintenance) as its final step. The agent asks briefly: **did anything mislead, surprise, or repeat? Was any instruction in `schema.md` or `AGENTS.md` wrong or missing? Did a reusable multi-step procedure emerge?** The answer is recorded as a single `- Lessons:` line in the day's `log.md` entry. No lesson → no line; it is never forced.

When a lesson is sharp, the agent **acts immediately**: it fixes a wrong `schema.md` claim on the spot, or creates/refines a skill. This is what makes the system self-updating — it edits its own constitution and toolkit, not just its notes. Everything softer waits for Sync consolidation.

### 2. Skills (autonomous capability growth)

Each skill is a folder with a `SKILL.md` (`name` + `description` frontmatter) describing one procedure the agent can reuse.

- **Create** a skill **autonomously** the moment a task surfaces a clearly reusable multi-step procedure — no need to be asked; the agent announces it when it does. Skills also emerge when Sync consolidation promotes a recurring `Lessons:` pattern.
- **Refine** an existing skill's `SKILL.md` when it underperforms in use, rather than spawning a near-duplicate.
- **Log** every skill creation or refinement in `log.md` with the keyword `skill`.

The one guardrail is restraint: every skill's `description` permanently occupies the agent's context window, so the toolkit is kept **few and sharp** — created eagerly, but pruned during Sync when a skill never fires.

### 3. Consolidate (weekly, during Sync)

The weekly Sync closes the loop: it reviews every `Lessons:` line logged since the last sync, promotes recurring patterns into new skills or `schema.md` amendments, refines skills that misfired, and prunes skills that never fire.

The result is a system that compounds on two axes at once: it accumulates knowledge *and* sharpens how it maintains that knowledge — without letting the toolkit metastasize.
