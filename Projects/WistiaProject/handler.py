"""
handler.py

AWS Lambda entry point for the Wistia ingestion pipeline.

Responsibilities
----------------
- Load the previous ingestion checkpoint
- Retrieve data from the Wistia API
- Apply incremental filtering where supported
- Store raw responses in the Bronze layer
- Update the ingestion checkpoint
"""

import json
from datetime import datetime, timezone

from config import MEDIA_IDS

from api import (
    fetch_media_data,
    fetch_visitors,
    fetch_events,
)

from pagination import fetch_all_pages

from checkpoint import (
    load_checkpoint,
    save_checkpoint,
)

from incremental import filter_incremental

from s3_writer import write_to_s3


# ==========================================================
# Lambda Handler
# ==========================================================

def lambda_handler(event, context):

    print("========================================")
    print("Starting Wistia ingestion pipeline")
    print("========================================")

    # ------------------------------------------------------
    # Load checkpoint
    # ------------------------------------------------------

    checkpoint = load_checkpoint()

    print(f"Loaded checkpoint: {checkpoint}")

    # ------------------------------------------------------
    # Media Statistics
    # ------------------------------------------------------

    media_records = []

    for media_id in MEDIA_IDS:

        print(f"Fetching media statistics: {media_id}")

        media_record = fetch_media_data(media_id)

        media_records.append(media_record)

    # Media Stats API returns current aggregate metrics only.
    # No timestamp exists for incremental filtering.
    write_to_s3(
        media_records,
        "media",
    )

    # ------------------------------------------------------
    # Visitors
    # ------------------------------------------------------

    print("Fetching visitors...")

    visitors = fetch_all_pages(
        fetch_visitors,
        max_pages=5
    )

    new_visitors = filter_incremental(
        records=visitors,
        checkpoint=checkpoint,
        timestamp_field="last_active_at",
    )

    write_to_s3(
        new_visitors,
        "visitors",
    )

    # ------------------------------------------------------
    # Events
    # ------------------------------------------------------

    all_events = []

    for media_id in MEDIA_IDS:

        print(f"Fetching events for media: {media_id}")

        events = fetch_all_pages(
            fetch_events,
            media_id=media_id,
            max_pages=5
        )

        all_events.extend(events)

    new_events = filter_incremental(
        records=all_events,
        checkpoint=checkpoint,
        timestamp_field="received_at",
    )

    write_to_s3(
        new_events,
        "events",
    )

    # ------------------------------------------------------
    # Save checkpoint
    # ------------------------------------------------------

    completion_time = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

    save_checkpoint(
        completion_time,
    )

    print("========================================")
    print("Pipeline completed successfully")
    print("========================================")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "status": "SUCCESS",
                "checkpoint": completion_time,
                "media_records": len(media_records),
                "visitor_records": len(new_visitors),
                "event_records": len(new_events),
            }
        ),
    }