"""
pagination.py

Reusable pagination utilities for the Wistia ingestion pipeline.

Responsible for:
- Fetching all pages from paginated API endpoints
- Preventing unnecessary API calls
- Providing consistent pagination behavior across endpoints

Implements FR6: Pagination handling.
"""

from config import DEFAULT_PAGE_SIZE


def fetch_all_pages(fetch_function, per_page=DEFAULT_PAGE_SIZE, max_pages=None, **kwargs):
    """
    Fetch all pages from a paginated API endpoint.

    Parameters
    ----------
    fetch_function : function
        API function responsible for retrieving a single page.
        Example:
            fetch_visitors(page=1, per_page=100)

    per_page : int
        Number of records requested per API call.

    **kwargs :
        Additional parameters required by the API function.
        Example:
            media_id="abc123"

    Returns
    -------
    list
        Combined list containing all records across all pages.
    """

    all_records = []

    page = 1

    while True:

        if max_pages is not None and page > max_pages:
            print(f"Reached max_pages={max_pages}")
            break

        records = fetch_function(
            page=page,
            per_page=per_page,
            **kwargs
        )

        # Safety check:
        # Some APIs may return None instead of an empty list.
        if not records:
            break

        all_records.extend(records)

        print(
            f"Pagination: page={page}, "
            f"records_received={len(records)}"
        )

        # If fewer records than requested are returned,
        # this is the final page.
        if len(records) < per_page:
            break

        page += 1

    print(
        f"Pagination complete. "
        f"Total records collected={len(all_records)}"
    )

    return all_records