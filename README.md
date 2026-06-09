# Nexus: Stateful Cognitive Infrastructure Template

A clean, open-source starter template for building a **Stateful Second Brain** using Obsidian, structured Markdown schemas, and CouchDB synchronization. This system transitions LLM interactions from stateless, ephemeral chat sessions into a compounding, persistent knowledge base.

---

## Core Philosophy

Standard Retrieval-Augmented Generation (RAG) is stateless—the AI agent starts fresh on every session, losing context over long intervals. The **Nexus Pattern** shifts this dynamic by giving the AI read and write access to a local, structured directory of markdown notes governed by a strict "constitution." 

Every session's code files, research briefs, and daily notes are parsed, cross-referenced, and compiled back into the database by the AI.

---

## Directory Structure

This template contains the following standard folder architecture for clean separation of concerns:

```
nexus/
├── schema.md          # System constitution (rules & conventions)
├── AGENTS.md          # Prompt guide/permissions for agent models
├── index.md           # Central hub cataloging all nodes
├── log.md             # Consolidated chronological operations log
├── assets/            # Graphs, diagrams, and static assets
├── sources/           # Summarized logs of raw ingest data (read-only)
├── projects/          # Multi-step execution plans and trackers
└── notes/             # Synthesized profiles on entities, concepts, and analyses
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
When using coding agents (such as Antigravity, Claude Code, or custom API wrappers), place the `AGENTS.md` system prompt inside the root directory. This acts as a sandbox boundary, directing the agent to write updates only into `wiki/` directories while enforcing schema rules.

### 3. Local Chunk-Level Synchronization (CouchDB)
To sync your markdown notes across devices securely and offline, use the CouchDB database sync configuration:
1. Spin up a local CouchDB Docker container:
   ```bash
   docker run -d -p 5984:5984 --name obsidian-couchdb couchdb
   ```
2. Configure a sync plugin (such as Obsidian Self-Hosted LiveSync) to connect to `http://localhost:5984/nexus`.
3. Map your `/etc/hosts` or local network to enable peer-to-peer replication between your phone and laptop.
