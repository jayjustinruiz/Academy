"""
s3_writer.py

Writes raw Wistia API responses to the Bronze layer in Amazon S3.

Responsibilities
----------------
- Serialize records as JSON
- Write to the Bronze S3 bucket
- Partition data by ingestion date
- Preserve raw API responses

Implements FR10: Store results in a structured data model.
"""

import json
import boto3

from datetime import datetime, timezone

from config import S3_BUCKET

# Initialize S3 client
s3 = boto3.client("s3")


def write_to_s3(data, dataset):
    """
    Write raw records to the Bronze S3 layer.

    Parameters
    ----------
    data : list | dict
        Raw API response to store.

    dataset : str
        Dataset name used as the S3 folder.
        Examples:
            media
            visitors
            events
    """

    # Current UTC timestamp
    now = datetime.now(timezone.utc)

    timestamp = now.strftime("%Y%m%dT%H%M%SZ")

    partition = now.strftime("%Y-%m-%d")

    key = (
        f"bronze/wistia/"
        f"{dataset}/"
        f"ingestion_date={partition}/"
        f"data_{timestamp}.json"
    )

    try:

        s3.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=json.dumps(data, default=str),
            ContentType="application/json"
        )

        print(
            f"S3 upload successful | "
            f"dataset={dataset} | "
            f"records={len(data) if isinstance(data, list) else 1} | "
            f"key={key}"
        )

    except Exception as e:
        raise RuntimeError(
            f"Failed to write {dataset} data to S3: {e}"
        ) from e