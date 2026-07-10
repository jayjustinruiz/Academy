"""
The checkpoint is stored as a JSON document in Amazon S3 and records
the timestamp of the last successful pipeline execution.
"""

import json

import boto3
from botocore.exceptions import ClientError

from config import (
    S3_BUCKET,
    CHECKPOINT_KEY,
)

# S3 client
s3 = boto3.client("s3")


def load_checkpoint():
    """
    Load the timestamp of the last successful ingestion.

    Returns
    -------
    str | None
        ISO-8601 timestamp representing the previous successful
        pipeline execution.

        Returns None if no checkpoint exists (first pipeline run).
    """

    try:
        response = s3.get_object(
            Bucket=S3_BUCKET,
            Key=CHECKPOINT_KEY,
        )

        checkpoint = json.loads(
            response["Body"].read()
        )

        return checkpoint.get("last_run")

    except ClientError as e:

        error_code = e.response["Error"]["Code"]

        # First pipeline execution
        if error_code == "NoSuchKey":
            print("Checkpoint not found. Starting full ingestion.")
            return None

        # Unexpected S3 error
        raise RuntimeError(
            f"Unable to load checkpoint from S3: {e}"
        ) from e

    except Exception as e:
        raise RuntimeError(
            f"Failed to load checkpoint: {e}"
        ) from e


def save_checkpoint(timestamp):
    """
    Save the timestamp of the latest successful ingestion.

    Parameters
    ----------
    timestamp : str
        ISO-8601 timestamp representing the successful completion
        of the current pipeline execution.
    """

    checkpoint = {
        "last_run": timestamp
    }

    try:

        s3.put_object(
            Bucket=S3_BUCKET,
            Key=CHECKPOINT_KEY,
            Body=json.dumps(checkpoint),
            ContentType="application/json",
        )

        print(f"Checkpoint updated: {timestamp}")

    except Exception as e:
        raise RuntimeError(
            f"Failed to save checkpoint: {e}"
        ) from e