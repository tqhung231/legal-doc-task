"""Ingestion entry point (starter stub).

Usage:
    python ingest.py data/feed.json

This is a starting point only — it does not implement the pipeline yet. Your job is to
fill it in. A typical run should:

    1. Read the feed (data/feed.json).
    2. Load each raw document from data/raw/.
    3. Normalize the text.
    4. Extract metadata (title, document number, type, authority, issue/effective dates...).
    5. Parse the legal structure (Chương / Mục / Điều / Khoản / Điểm).
    6. Detect duplicates vs updated versions (content hash + document number).
    7. Record quality warnings instead of failing silently.
    8. Save documents, versions, and one ingestion-run record to a database.

See README.md for the full task description.
"""

import argparse


def main(feed_path: str) -> None:
    # TODO: implement the ingestion pipeline (see the steps in the module docstring).
    raise NotImplementedError(
        f"Ingestion not implemented yet. Feed: {feed_path}. See README.md."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a feed of legal documents.")
    parser.add_argument("feed", help="Path to the feed JSON file (e.g. data/feed.json).")
    args = parser.parse_args()
    main(args.feed)
