#!/usr/bin/env python3
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import os


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert problems.csv to JSON format."
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="data/problems.csv",
        help="Path to the input CSV file (default: data/problems.csv)"
    )
    parser.add_argument(
        "--problems-json",
        type=str,
        default="data/problems.json",
        help="Path to the output problems JSON file (default: data/problems.json)"
    )
    parser.add_argument(
        "--concepts-json",
        type=str,
        default="data/concepts.json",
        help="Path to the output concepts JSON file (default: data/concepts.json)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print the JSON output"
    )

    return parser.parse_args()


def read_csv(file_path: str) -> Dict[str, Any]:
    """Read the CSV file and convert it to a list of dictionaries and unique concepts."""
    problems = []
    unique_concepts = set()

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 5:

                    # Split concepts and datastructures by semicolon instead of comma
                    concept_streams  = [c.strip() for c in row[2].split(';')] if row[2] else []
                    datastructure_streams = [d.strip() for d in row[3].split(';')] if row[3] else []


                    problem = {
                        "id": int(row[0]),
                        "description": row[1],
                        "concepts": concept_streams,
                        "datastructure": datastructure_streams,
                        "approach": row[4]
                    }
                    problems.append(problem)
                else:
                    print(f"Warning: Skipping row with insufficient columns: {row}", file=sys.stderr)
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        sys.exit(1)


    return problems

def write_json(problems: List[Dict[str, Any]], output_path: Optional[str], pretty: bool = False) -> None:
    """Write the problems list to JSON format."""
    indent = 4 if pretty else None

    try:
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(problems, jsonfile, indent=indent)
            print(f"JSON data written to {output_path}")
        else:
            # Write to stdout
            print(json.dumps(problems, indent=indent))
    except Exception as e:
        print(f"Error writing JSON: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main function to convert CSV to JSON."""

    version = 0
    input_dir = Path('data')

    # Find the highest version number
    while (input_dir / f"problems_v{version+1}.csv").exists():
        version += 1

    # Use the highest version file
    input_file = str(input_dir / f"problems_v{version}.csv")
    print(f"Using highest version file: {input_file}")
    data = read_csv(input_file)

    # Write to JSON with the same version number
    output_json = f"data/problems_v{version}.json"
    write_json(data, output_json, pretty=True)

if __name__ == "__main__":
    main()
