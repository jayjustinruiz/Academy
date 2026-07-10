"""
This module filters API records based on a configurable timestamp field
and the timestamp of the previous successful pipeline execution.
"""

from datetime import datetime
from typing import List, Dict, Optional


def filter_incremental(
    records: List[Dict],
    checkpoint: Optional[str],
    timestamp_field: str,
) -> List[Dict]:
    """
    Return only records newer than the checkpoint.

    Parameters
    ----------
    records : list[dict]
        Records returned by the API.

    checkpoint : str | None
        Timestamp of the previous successful ingestion.
        If None, all records are returned (first pipeline run).

    timestamp_field : str
        Name of the timestamp field in each record
        (e.g. 'last_active_at', 'received_at').

    Returns
    -------
    list[dict]
        Records newer than the checkpoint.
    """

    # ----------------------------------------------------
    # First pipeline execution
    # ----------------------------------------------------
    if checkpoint is None:
        return records

    checkpoint_dt = datetime.fromisoformat(
        checkpoint.replace("Z", "+00:00")
    )

    filtered = []

    for record in records:

        timestamp = record.get(timestamp_field)

        # Skip records missing the timestamp field
        if not timestamp:
            continue

        try:
            record_dt = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )

            if record_dt > checkpoint_dt:
                filtered.append(record)

        except (ValueError, TypeError):
            # Ignore malformed timestamps
            continue

    return filtered