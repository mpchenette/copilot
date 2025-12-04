#!/usr/bin/env python3
import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


def parse_surface(surface: str):
    """
    Parse a Last Surface Used value like:
      - "vscode/1.99.3/copilot-chat/0.26.7"
      - "JetBrains-IC/251.26927.53/"
      - "VisualStudio/17.8.21/copilot-vs/1.206.0.0"

    Returns (ide_name, ide_version, ext_name, ext_version) where ext_* can be None.
    Whitespace is stripped; empty or 'None' values return (None, None, None, None).
    """
    if surface is None:
        return None, None, None, None
    s = str(surface).strip()
    if not s or s.lower() == "none":
        return None, None, None, None

    # Split by '/', keep empty tokens to allow trailing slash patterns
    parts = s.split('/')
    parts = [p.strip() for p in parts]
    parts = [p for p in parts if p != '']  # drop empty tokens from trailing '/'

    if len(parts) < 2:
        return None, None, None, None

    ide_name, ide_version = parts[0], parts[1]
    ext_name = ext_version = None
    if len(parts) >= 4:
        ext_name, ext_version = parts[2], parts[3]

    return ide_name, ide_version, ext_name, ext_version


from typing import Optional


def is_copilot_extension(name: Optional[str]) -> bool:
    if not name:
        return False
    return name.lower().startswith("copilot")


def find_default_csv() -> Optional[Path]:
    # Look for a seat activity CSV in ./scripts by default
    cand_dir = Path(__file__).resolve().parent
    matches = sorted(cand_dir.glob("seat-activity-*.csv"))
    if matches:
        # Choose the lexicographically last; filename usually contains a timestamp
        return matches[-1]
    return None


def main():
    parser = argparse.ArgumentParser(description="Report counts of IDE versions and Copilot extension versions from seat activity CSV.")
    parser.add_argument("csv_path", nargs="?", help="Path to CSV (defaults to scripts/seat-activity-*.csv)")
    parser.add_argument("--by-extension-name", action="store_true", help="Also break down Copilot counts by extension name (e.g., copilot, copilot-chat, copilot-intellij).")
    parser.add_argument("--write-csv", action="store_true", help="Write results to CSV files alongside the input or to --out-dir.")
    parser.add_argument("--out-dir", help="Directory to write CSV files. Defaults to the input CSV's directory.")
    parser.add_argument("--prefix", help="Output filename prefix. Defaults to the input CSV filename stem.")
    args = parser.parse_args()

    csv_path = args.csv_path
    if not csv_path:
        default = find_default_csv()
        if not default:
            print("No CSV provided and no default seat activity CSV found in scripts/", file=sys.stderr)
            sys.exit(1)
        csv_path = str(default)

    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"CSV not found: {csv_file}", file=sys.stderr)
        sys.exit(1)

    ide_counts = Counter()
    copilot_version_counts = Counter()
    copilot_name_version_counts = Counter()  # optional detailed breakdown
    malformed_surfaces = 0
    empty_surfaces = 0

    with csv_file.open(newline='') as f:
        reader = csv.DictReader(f)
        # try to detect the column name case-insensitively
        header_map = {h.lower(): h for h in reader.fieldnames or []}
        surface_col = None
        for key in ("last surface used", "last_surface_used", "surface", "lastsurfaceused"):
            if key in header_map:
                surface_col = header_map[key]
                break
        if surface_col is None:
            print("Could not find 'Last Surface Used' column in CSV headers.", file=sys.stderr)
            sys.exit(1)

        for row in reader:
            raw_surface = row.get(surface_col)
            ide_name, ide_ver, ext_name, ext_ver = parse_surface(raw_surface)
            if ide_name is None or ide_ver is None:
                if raw_surface and raw_surface.strip().lower() != "none":
                    malformed_surfaces += 1
                else:
                    empty_surfaces += 1
                continue

            # Normalize IDE name to lower for grouping consistency
            norm_ide_name = ide_name.lower()
            ide_key = f"{norm_ide_name}/{ide_ver}"
            ide_counts[ide_key] += 1

            if is_copilot_extension(ext_name) and ext_ver:
                copilot_version_counts[ext_ver] += 1
                name_ver_key = f"{ext_name.lower()}/{ext_ver}"
                copilot_name_version_counts[name_ver_key] += 1

    def print_counter(title: str, counter: Counter):
        print(title)
        for key, count in counter.most_common():
            print(f"  {key}: {count}")
        if not counter:
            print("  (none)")
        print()

    print(f"Source: {csv_file}")
    print()
    print_counter("IDE Versions (name/version):", ide_counts)
    print_counter("Copilot Extension Versions (by version):", copilot_version_counts)
    if args.by_extension_name:
        print_counter("Copilot Extension Versions (by extension name/version):", copilot_name_version_counts)

    # Optionally write results to CSV files
    if args.write_csv:
        out_dir = Path(args.out_dir) if args.out_dir else csv_file.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        prefix = args.prefix if args.prefix else csv_file.stem

        ide_out = out_dir / f"{prefix}_ide_versions.csv"
        copilot_out = out_dir / f"{prefix}_copilot_versions.csv"
        copilot_byname_out = out_dir / f"{prefix}_copilot_extname_versions.csv"

        # Write IDE versions as columns: ide_name, ide_version, count
        with ide_out.open('w', newline='') as f:
            w = csv.writer(f)
            w.writerow(["ide_name", "ide_version", "count"])
            for key, count in ide_counts.most_common():
                ide_name, ide_version = key.split('/', 1) if '/' in key else (key, "")
                w.writerow([ide_name, ide_version, count])

        # Write Copilot versions as columns: extension_version, count
        with copilot_out.open('w', newline='') as f:
            w = csv.writer(f)
            w.writerow(["extension_version", "count"])
            for ver, count in copilot_version_counts.most_common():
                w.writerow([ver, count])

        # Optional: by extension name and version
        if args.by_extension_name:
            with copilot_byname_out.open('w', newline='') as f:
                w = csv.writer(f)
                w.writerow(["extension_name", "extension_version", "count"])
                for key, count in copilot_name_version_counts.most_common():
                    ext_name, ext_version = key.split('/', 1) if '/' in key else (key, "")
                    w.writerow([ext_name, ext_version, count])

        print("Written CSVs:")
        print(f"  {ide_out}")
        print(f"  {copilot_out}")
        if args.by_extension_name:
            print(f"  {copilot_byname_out}")

    # Small diagnostic footer
    if malformed_surfaces or empty_surfaces:
        print("Notes:")
        if empty_surfaces:
            print(f"  Rows with empty/None surface: {empty_surfaces}")
        if malformed_surfaces:
            print(f"  Rows with unparseable surface: {malformed_surfaces}")


if __name__ == "__main__":
    main()
