#!/usr/bin/env python3
"""Check whether an xlsx is small enough to upload to Google Drive as a native Google Sheet.

Usage:
    python upload_to_drive.py output.xlsx "GEO Action Plan - <scope>"
    python upload_to_drive.py output.xlsx "..." --payload-out payload.txt

Drive converts an uploaded xlsx into a multi-tab Google Sheet when the upload
uses the xlsx MIME type and leaves conversion to Google formats on. Through a
connector, the file has to travel inline as base64, copied character for
character into the upload call. A single wrong character corrupts the file, so
this script only approves payloads short enough to copy exactly.

The script never uploads anything. It reports the payload size and, when the
file is small enough, what to pass to the Google Drive connector's file-upload
tool.
"""

import argparse
import base64
import os
import sys

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

# Payloads longer than this can't be copied reliably into a tool call.
# Keep in sync with the "Google Sheet" paragraph in SKILL.md.
LIMIT = 20_000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("title")
    ap.add_argument("--payload-out", help="write the base64 payload to this file")
    args = ap.parse_args()

    if not os.path.exists(args.xlsx):
        sys.exit(f"No such file: {args.xlsx}")

    raw = open(args.xlsx, "rb").read()
    payload = base64.b64encode(raw).decode()
    chars = len(payload)
    print(f"File: {args.xlsx} ({len(raw) / 1024:.0f} KB, {chars:,} base64 characters; limit {LIMIT:,})")

    if chars > LIMIT:
        print(
            "\nTOO LARGE to upload through a connector. Deliver the xlsx as the plan, and tell the\n"
            "user it opens as a Google Sheet once they upload it to Google Drive themselves."
        )
        sys.exit(2)

    if args.payload_out:
        with open(args.payload_out, "w") as f:
            f.write(payload)
        print(f"Payload written to {args.payload_out}")

    print(
        "\nSmall enough to upload. With the Google Drive connector's file-upload tool, create a file with:\n"
        f"  - name: {args.title}\n"
        f"  - MIME type: {XLSX_MIME}\n"
        f"  - content: the base64 payload{' in ' + args.payload_out if args.payload_out else ''}, copied exactly\n"
        "  - conversion to Google formats left on, so Drive turns it into a Google Sheet\n"
        "Send the user the xlsx as well, so they have the complete file whatever the Sheet holds."
    )


if __name__ == "__main__":
    main()
