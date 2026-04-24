import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

# Matches Failed password and Invalid user patterns
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*?:\s"
    r"(?:Failed password for (?:invalid user )?(?P<failed_user>\S+)|"
    r"Invalid user (?P<invalid_user>\S+))\s"
    r"from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parses the log file and extracts suspicious login attempts."
    )

    parser.add_argument("input_file", help="Path to the log file to be parsed")

    parser.add_argument(
        "-o",
        "--output",
        default="suspect.csv",
        help="Path to the output CSV file",
    )

    return parser.parse_args()


def parse_log(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"Error: file {file_path} does not exist", file=sys.stderr)
        sys.exit(1)

    records = []
    current_year = datetime.now().year

    with path.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = LOG_PATTERN.search(line)
            if not match:
                continue

            # Skip successful logins
            if "Accepted password" in line:
                continue

            # Correct user extraction (important fix)
            user = match.group("failed_user") or match.group("invalid_user")

            timestamp = datetime.strptime(
                match.group("timestamp"), "%b %d %H:%M:%S"
            ).replace(year=current_year)

            records.append(
                {
                    "Timestamp": timestamp.strftime("%b %d %H:%M:%S"),
                    "IP_Address": match.group("ip"),
                    "User_Account": user,
                }
            )

    return records


def remove_duplicates(records):
    seen = set()
    unique = []

    for r in records:
        key = (r["Timestamp"], r["IP_Address"], r["User_Account"])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique


def write_csv(records, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Timestamp", "IP_Address", "User_Account"]
        )
        writer.writeheader()
        writer.writerows(records)


def main():
    args = parse_arguments()

    records = parse_log(args.input_file)
    records = remove_duplicates(records)
    write_csv(records, args.output)


if __name__ == "__main__":
    main()
