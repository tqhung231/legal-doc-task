# Sample data

These files are a **synthetic, fabricated** corpus created for this take-home task. The
documents are **not real Vietnamese legal documents** — the texts, document numbers, dates,
and signatories are invented. They imitate the format and structure of real legal documents
(header block, `Căn cứ…` preamble, `Chương`/`Mục`/`Điều`/`Khoản`/`Điểm`, signature block)
so you can build and test a realistic ingestion pipeline without scraping any live source.

## Layout

```
data/
  feed.json        # the ingestion feed — start here
  raw/             # raw document text files referenced by the feed
```

## feed.json

A JSON array. Each entry describes one document to ingest:

| Field           | Meaning                                                              |
|-----------------|----------------------------------------------------------------------|
| `source_url`    | Where the document supposedly came from (synthetic).                 |
| `raw_file`      | File under `raw/` containing the raw document text.                  |
| `expected_type` | A **loose hint** about the document type from the source listing.    |

`expected_type` is only a hint. It may be `null`, and it is not guaranteed to be correct —
your pipeline should still determine the real document type from the document text itself
and record a warning if they disagree.

## What's in the corpus

The dataset deliberately includes messy and tricky cases — duplicates, an amended law, a
re-issued document, a document missing a field, and a badly formatted file. Part of the task
is handling them gracefully (see the root `README.md`). Figuring out *which* file is *which*
case is part of the exercise.
