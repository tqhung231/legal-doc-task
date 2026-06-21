# Take-Home Task: Legal Document Intake Pipeline + QA Console

*(Phiên bản tiếng Việt: [README.vi.md](README.vi.md))*

## Context

Our product works with Vietnamese legal documents and uses them later for search / RAG.
Before documents enter the RAG pipeline, we need a **staging system** that receives new or
changed legal documents, normalizes them, extracts metadata, detects duplicates/updates, and
lets a reviewer inspect the result.

This repo gives you everything you need to start: a small **synthetic** corpus of legal
documents (`data/`) and a thin project skeleton. You build the pipeline and a simple
inspection UI on top of it.

> You do **not** need to build a crawler, real embeddings, or a full RAG system. This task is
> about clean data modeling, a repeatable ingestion pipeline, legal-document understanding,
> and inspectability.

## Goal

Build a small app that:

1. Ingests the local feed of legal documents in `data/feed.json`.
2. Stores them in a database.
3. Parses their legal structure (`Chương` / `Mục` / `Điều` / `Khoản` / `Điểm`).
4. Detects duplicates and updated versions.
5. Provides a simple UI to inspect the extracted metadata and text quality.

## Requirements

### 1. Ingestion

Implement an ingestion command (or API) that reads `data/feed.json`, loads each raw legal
text file from `data/raw/`, and saves the result into a database. A starting entry point is
provided at [`ingest.py`](ingest.py):

```bash
python ingest.py data/feed.json
```

For each document, store at least: raw text, normalized text, source URL, content hash, and
an **ingestion status** of `new`, `duplicate`, `updated`, or `failed`.

The ingestion must be **idempotent**: running the same input twice must not create duplicate
documents. Suggested logic:

```
same document_number + same content_hash       -> duplicate
same document_number + different content_hash   -> updated version
new document_number                             -> new document
```

### 2. Metadata extraction

Extract at least: `title`, `document_number`, `document_type`, `issuing_authority`,
`issue_date`, `effective_date`, and `status` if available. If a field cannot be extracted,
store `null` and record a **warning** instead of failing silently.

### 3. Legal structure parsing

Parse the document into legal structure and store it as JSON.

- **Minimum:** `Điều`, `Khoản`
- **Bonus:** `Chương`, `Mục`, `Điểm`

This matters for legal RAG: chunking by arbitrary token windows is poor; legal text should be
chunked around meaningful units (article, clause, point).

### 4. Quality issues

Record warnings for problems such as: missing document number, missing effective date,
duplicate document, failed structure parsing, or a possible amended/replaced document that was
detected but not linked.

### 5. UI

Build a simple inspection UI with:

- an **ingestion-run list** (when, totals, new/updated/duplicate/failed counts, warnings),
- a **document list** (title, number, type, authority, dates, status, ingestion status) with
  basic filtering,
- a **document detail page** showing extracted metadata, raw vs normalized text, the parsed
  legal-structure tree, warnings, related documents, and — if implemented — a RAG-chunk preview.

The point of the UI is **inspectability**, not beauty: can a reviewer quickly tell whether the
pipeline extracted the law correctly?

### 6. README

In your submission, explain how to install dependencies, run any DB migration, run ingestion,
start the UI, and the reasoning behind your schema and design choices.

## Heads-up about the data

The corpus in `data/` is intentionally tricky. It contains, among other things: a clean
well-structured law, duplicates, a law that amends an earlier one, a re-issued document, a
document missing a field, and a badly formatted file. Your pipeline should handle all of them
gracefully — **one bad document must not break the whole run.** See
[`data/README.md`](data/README.md) for the feed format.

## Bonus

- Extract related documents from phrases like `sửa đổi, bổ sung`, `thay thế`, `hướng dẫn`.
- Generate RAG-ready chunks per legal unit (article/clause), with metadata attached.
- Add search by title, document number, and article text.
- Add basic tests for metadata extraction and duplicate detection (a `tests/` folder is set up).

## Suggested stack (not required)

The repo is set up as a Python project, so a natural choice is **Python + SQLite + a simple UI**
(e.g. Streamlit or Flask). You are free to use another language, database, or framework — if you
do, just keep `data/` as the input and explain your setup in your README. Dependency suggestions
are listed (commented) in [`pyproject.toml`](pyproject.toml).

## Getting started

```bash
# 1. (suggested) create an environment and install deps you choose
uv sync                 # or: python -m venv .venv && pip install ...

# 2. run the ingestion entry point against the feed
python ingest.py data/feed.json

# 3. build out the pipeline, database, and UI from here
```

## What we value

We care more about **clean data modeling, repeatable ingestion, and legal-document
understanding** than UI polish. Show your thinking in your schema, your handling of messy/missing
data, and your README. Scope this as roughly a **1–2 day** take-home.
