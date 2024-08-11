#!/usr/bin/python3
"""
markdown2html.py

This script converts a Markdown file to an HTML file.
"""

import sys
import os
import markdown


def main():
    """
    Check the number of arguments
    Extract arguments
    Check if the Markdown file exists
    Read the Markdown file
    Convert Markdown to HTML
    and Write the HTML content to the output file
    """
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

        markdown_file = sys.argv[1]
        html_file = sys.argv[2]

        if not os.path.isfile(markdown_file):
            print(f"Missing {markdown_file}", file=sys.stderr)
            sys.exit(1)

        with open(markdown_file, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()

        html_content = markdown.markdown(md_content)

        with open(html_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

        sys.exit(0)


if __name__ == "__main__":
    main()
