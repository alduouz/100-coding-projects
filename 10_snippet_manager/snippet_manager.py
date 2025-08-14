#!/usr/bin/env python3
import argparse
import json
import os
import uuid
import datetime
import tempfile
import sys


def load_snippets(file_path):
    """Load snippets from JSON file. Return empty list if file doesn't exist."""
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_snippets(snippets, file_path):
    """Save snippets to JSON file atomically."""
    temp_file = file_path + '.tmp'
    try:
        with open(temp_file, 'w') as f:
            json.dump(snippets, f, indent=2, default=str)
        os.rename(temp_file, file_path)
    except IOError as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise e


def add_snippet(file_path, description=None, code=None, tags=None):
    """Add a new snippet to storage."""
    if not description:
        description = input("Enter snippet description: ").strip()
    if not description:
        print("Error: Description is required")
        return False
    
    if not code:
        print("Enter snippet code (press Ctrl+D or Ctrl+Z when done):")
        code_lines = []
        try:
            while True:
                line = input()
                code_lines.append(line)
        except EOFError:
            pass
        code = '\n'.join(code_lines).strip()
    
    if not code:
        print("Error: Code is required")
        return False
    
    if tags is None:
        tags_input = input("Enter tags (comma-separated, optional): ").strip()
        tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()] if tags_input else []
    elif isinstance(tags, str):
        tags = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
    
    snippet = {
        'id': str(uuid.uuid4()),
        'description': description,
        'code': code,
        'tags': tags,
        'created_at': datetime.datetime.now().isoformat()
    }
    
    snippets = load_snippets(file_path)
    snippets.append(snippet)
    save_snippets(snippets, file_path)
    print(f"Snippet added with ID: {snippet['id']}")
    return True


def list_snippets(file_path):
    """List all snippets."""
    snippets = load_snippets(file_path)
    if not snippets:
        print("No snippets found.")
        return
    
    for snippet in snippets:
        created_date = datetime.datetime.fromisoformat(snippet['created_at']).strftime('%Y-%m-%d %H:%M')
        tags_str = ', '.join(snippet['tags']) if snippet['tags'] else 'None'
        print(f"ID: {snippet['id']}")
        print(f"Description: {snippet['description']}")
        print(f"Tags: {tags_str}")
        print(f"Created: {created_date}")
        print(f"Code:\n{snippet['code']}")
        print("-" * 50)


def search_snippets(file_path, keyword):
    """Search snippets by keyword in description, code, or tags."""
    snippets = load_snippets(file_path)
    keyword_lower = keyword.lower()
    matches = []
    
    for snippet in snippets:
        if (keyword_lower in snippet['description'].lower() or
            keyword_lower in snippet['code'].lower() or
            any(keyword_lower in tag for tag in snippet['tags'])):
            matches.append(snippet)
    
    if not matches:
        print(f"No snippets found matching '{keyword}'")
        return
    
    print(f"Found {len(matches)} snippet(s) matching '{keyword}':")
    print("-" * 50)
    
    for snippet in matches:
        created_date = datetime.datetime.fromisoformat(snippet['created_at']).strftime('%Y-%m-%d %H:%M')
        tags_str = ', '.join(snippet['tags']) if snippet['tags'] else 'None'
        print(f"ID: {snippet['id']}")
        print(f"Description: {snippet['description']}")
        print(f"Tags: {tags_str}")
        print(f"Created: {created_date}")
        print(f"Code:\n{snippet['code']}")
        print("-" * 50)


def export_snippets(file_path, format_type, output_file=None):
    """Export snippets to markdown or text format."""
    snippets = load_snippets(file_path)
    if not snippets:
        print("No snippets to export.")
        return
    
    if not output_file:
        output_file = f"snippets_export.{format_type}"
    
    content = []
    
    if format_type == 'md':
        content.append("# Code Snippets\n")
        for snippet in snippets:
            created_date = datetime.datetime.fromisoformat(snippet['created_at']).strftime('%Y-%m-%d %H:%M')
            tags_str = ', '.join(snippet['tags']) if snippet['tags'] else 'None'
            content.append(f"## {snippet['description']}\n")
            content.append(f"**ID:** {snippet['id']}  ")
            content.append(f"**Tags:** {tags_str}  ")
            content.append(f"**Created:** {created_date}\n")
            content.append("```")
            content.append(snippet['code'])
            content.append("```\n")
    
    elif format_type == 'txt':
        content.append("CODE SNIPPETS\n")
        content.append("=" * 50 + "\n")
        for snippet in snippets:
            created_date = datetime.datetime.fromisoformat(snippet['created_at']).strftime('%Y-%m-%d %H:%M')
            tags_str = ', '.join(snippet['tags']) if snippet['tags'] else 'None'
            content.append(f"Description: {snippet['description']}")
            content.append(f"ID: {snippet['id']}")
            content.append(f"Tags: {tags_str}")
            content.append(f"Created: {created_date}")
            content.append("Code:")
            content.append(snippet['code'])
            content.append("-" * 50 + "\n")
    
    try:
        with open(output_file, 'w') as f:
            f.write('\n'.join(content))
        print(f"Snippets exported to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Manage code snippets")
    parser.add_argument('--file', default='snippets.json', help='JSON file to store snippets')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    add_parser = subparsers.add_parser('add', help='Add a new snippet')
    add_parser.add_argument('--file', default='snippets.json', help='JSON file to store snippets')
    add_parser.add_argument('--description', help='Snippet description')
    add_parser.add_argument('--code', help='Snippet code')
    add_parser.add_argument('--tags', help='Comma-separated tags')
    
    list_parser = subparsers.add_parser('list', help='List all snippets')
    list_parser.add_argument('--file', default='snippets.json', help='JSON file to store snippets')
    
    search_parser = subparsers.add_parser('search', help='Search snippets by keyword')
    search_parser.add_argument('keyword', help='Keyword to search for')
    search_parser.add_argument('--file', default='snippets.json', help='JSON file to store snippets')
    
    export_parser = subparsers.add_parser('export', help='Export snippets')
    export_parser.add_argument('--file', default='snippets.json', help='JSON file to store snippets')
    export_parser.add_argument('--format', choices=['md', 'txt'], default='md', help='Export format')
    export_parser.add_argument('--output', help='Output file name')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'add':
        add_snippet(args.file, args.description, args.code, args.tags)
    elif args.command == 'list':
        list_snippets(args.file)
    elif args.command == 'search':
        search_snippets(args.file, args.keyword)
    elif args.command == 'export':
        export_snippets(args.file, args.format, args.output)


if __name__ == '__main__':
    main()