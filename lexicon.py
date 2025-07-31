#!/usr/bin/env python3
import os
import re
import sys

def get_frontmatter_and_content(file_path):
    """Extract frontmatter and remaining content from the file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)', content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1), match.group(2)

def escape_yaml_string(s):
    """Escape double quotes for YAML."""
    return s.replace('"', '\\"')

def build_entry(term, definition, stressed):
    term_esc = escape_yaml_string(term)
    def_esc = escape_yaml_string(definition)
    stressed_esc = escape_yaml_string(stressed)
    return f'  - term: "{term_esc}"\n    definition: "{def_esc}"\n    stressed: "{stressed_esc}"'

def insert_into_frontmatter(frontmatter, new_entries):
    """Insert entries under lexicon: (create if not present)."""
    if re.search(r'^\s*lexicon:\s*$', frontmatter, flags=re.MULTILINE):
        # Simple case: lexicon: exists but no entries yet
        return re.sub(r'^\s*lexicon:\s*$', 'lexicon:\n' + "\n".join(new_entries),
                      frontmatter, count=1, flags=re.MULTILINE)

    match = re.search(r'(lexicon:\s*(?:\n(?:[ \t]+-.*?)+))', frontmatter, flags=re.DOTALL)
    if match:
        # Append to existing list
        block = match.group(1).rstrip()
        updated_block = block + "\n" + "\n".join(new_entries)
        return frontmatter[:match.start(1)] + updated_block + frontmatter[match.end(1):]
    else:
        # No lexicon section at all: append it at the end
        suffix = ("\n" if not frontmatter.endswith("\n") else "") + "lexicon:\n" + "\n".join(new_entries)
        return frontmatter + suffix

def is_monosyllabic(word):
    """Heuristic: if only one vowel group, treat as monosyllabic."""
    vowel_groups = re.findall(r'[aeiouy]+', word.lower())
    return len(vowel_groups) <= 1

def add_lexicon_entries(file_path):
    frontmatter_text, remaining_content = get_frontmatter_and_content(file_path)
    if frontmatter_text is None:
        print(f"Error: Could not find frontmatter in {file_path}")
        return

    new_entries = []
    print("\nAdding new lexicon entries. Type 'done' to finish.")
    while True:
        term_input = input("\nEnter term (or 'done' to finish): ").strip()
        if term_input.lower() == 'done':
            break

        definition = input("Enter definition: ").strip()

        if '*' in term_input:
            stressed = term_input
            term = term_input.replace('*', '')
        else:
            term = term_input
            if is_monosyllabic(term):
                stressed = term
            else:
                stressed = input("Enter stressed form (e.g., ch*apter): ").strip()

        entry_text = build_entry(term, definition, stressed)
        new_entries.append(entry_text)
        print(f"Added: term='{term}' definition='{definition}' stressed='{stressed}'")

    if not new_entries:
        print("No entries added.")
        return

    updated_frontmatter = insert_into_frontmatter(frontmatter_text, new_entries)

    # Backup original
    backup_path = file_path + ".bak"
    with open(backup_path, 'w', encoding='utf-8') as bak, open(file_path, 'r', encoding='utf-8') as orig:
        bak.write(orig.read())

    # Write updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"---\n{updated_frontmatter}\n---\n{remaining_content}")

    print(f"\nFile updated successfully. Backup saved as {backup_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 lexicon.py <path_to_markdown_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    add_lexicon_entries(file_path)

if __name__ == "__main__":
    main()

