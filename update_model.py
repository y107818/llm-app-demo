#!/usr/bin/env python3
import argparse
import os
import re
from glob import glob


def update_model_name(path: str, new_model: str):
    changed = []
    pattern = re.compile(r'(llm_config\s*:\s*\{[^{}]*?model_name\s*:\s*)([^,\s}]+)')
    for fname in glob(os.path.join(path, '**', '*.hocon'), recursive=True):
        with open(fname, 'r', encoding='utf-8') as f:
            text = f.read()
        new_text, count = pattern.subn(r"\1" + new_model, text)
        if count:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(new_text)
            changed.append(fname)
    return changed


def main():
    parser = argparse.ArgumentParser(description="Update model name in HOCON files")
    subparsers = parser.add_subparsers(dest="command")
    up = subparsers.add_parser("update-model", help="Update model name in .hocon files")
    up.add_argument("model_name", help="Model name to set")
    up.add_argument("--path", default=".", help="Directory to search for .hocon files")

    args = parser.parse_args()

    if args.command == "update-model":
        changed = update_model_name(args.path, args.model_name)
        if changed:
            print(f"Updated model name in {len(changed)} file(s).")
        else:
            print("No matching model_name fields found.")


if __name__ == "__main__":
    main()
