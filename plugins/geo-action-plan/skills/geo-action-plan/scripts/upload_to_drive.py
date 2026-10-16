#!/usr/bin/env python3
"""Prepare an xlsx for upload to Google Drive as a native Google Sheet.

Usage:
    python upload_to_drive.py output.xlsx "GEO Action Plan — <scope>"
    python upload_to_drive.py output.xlsx "..." --payload-out payload.txt

Drive converts an uploaded xlsx into a real multi-tab Google Sheet automatically,
provided contentMimeType is the xlsx type and conversion is left enabled. The
content has to travel inline as base64 through the tool call, which is the
binding constraint: a large workbook produces a payload too big to pass.

This script base64-encodes the file, reports the payload size, and tells you
whether to upload the whole thing or cap a tab first. It never uploads by
itself — it prints the exact arguments for the Google Drive create_file tool.
"""

import argparse
import base64
import json
import os
import sys

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

# Payload characters that comfortably fit through a tool call. Past the soft
# limit the upload gets expensive; past the hard limit it will not go through.
SOFT_LIMIT = 400_000
HARD_LIMIT = 900_000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("title")
    ap.add_argument("--parent-id", help="Drive folder id to upload into")
    ap.add_argument("--payload-out", help="write the base64 payload to this file")
    args = ap.parse_args()

    if not os.path.exists(args.xlsx):
        sys.exit(f"No such file: {args.xlsx}")

    raw = open(args.xlsx, "rb").read()
    payload = base64.b64encode(raw).decode()
    size_kb = len(raw) / 1024
    chars = len(payload)

    print(f"File: {args.xlsx}  ({size_kb:.0f} KB on disk, {chars:,} base64 characters)")

    if chars > HARD_LIMIT:
        print(
            "\nTOO LARGE to pass through a tool call.\n"
            "Deliver the full workbook as a download instead, and build a trimmed copy for the\n"
            "Sheet — the SERP Pages tab is almost always the culprit. Cap it to the top few\n"
            "hundred rows, rebuild, and re-run this script. Say clearly in chat that the Sheet\n"
            "is capped and the xlsx is complete."
        )
        sys.exit(2)

    if chars > SOFT_LIMIT:
        print(
            "\nLarge payload — it will go through, but consider capping the SERP Pages tab if\n"
            "the user mainly wants the plan tabs in the Sheet."
        )

    if args.payload_out:
        with open(args.payload_out, "w") as f:
            f.write(payload)
        print(f"\nPayload written to {args.payload_out}")

    print("\nCall Google Drive create_file with:")
    print(
        json.dumps(
            {
                "title": args.title,
                "contentMimeType": XLSX_MIME,
                "base64Content": f"<contents of {args.payload_out or 'the payload'}>",
                **({"parentId": args.parent_id} if args.parent_id else {}),
            },
            indent=2,
        )
    )
    print(
        "\nLeave disableConversionToGoogleType unset — conversion is what turns the xlsx into a\n"
        "native Sheet with one tab per worksheet. Present the xlsx to the user as well, so they\n"
        "have the complete data regardless of what the Sheet holds."
    )


if __name__ == "__main__":
    main()
