#!/usr/bin/python3
''' Write a script markdown2html.py that takes an argument 2 strings:
    First argument is the name of the Markdown file
    Second argument is the output file name
'''

import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            unordered_start, ordered_start, paragraph = False, False, False
            for line in read:
                # Handle bold and italic text
                line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)

                # Handle MD5 hashing of text within [[text]]
                md5 = re.findall(r'\[\[.+?\]\]', line)
                if md5:
                    md5_content = re.findall(r'\[\[(.+?)\]\]', line)[0]
                    line = line.replace(md5[0],
                                        hashlib.md5(md5_content.encode())
                                        .hexdigest())

                # Remove the letter C or c in text within ((text))
                remove_letter_c = re.findall(r'\(\(.+?\)\)', line)
                if remove_letter_c:
                    clean_content = re.findall(r'\(\((.+?)\)\)', line)[0]
                    clean_content = ''.join(
                        char for char in clean_content if char.lower() != 'c')
                    line = line.replace(remove_letter_c[0], clean_content)

                # Handle headings
                heading_level = len(line) - len(line.lstrip('#'))
                if 1 <= heading_level <= 6:
                    line = ('<h{}>{}</h{}>\n'.format(
                        heading_level, line.strip('#').strip(), heading_level))

                # Handle unordered lists
                if line.startswith('- '):
                    if not unordered_start:
                        html.write('<ul>\n')
                        unordered_start = True
                    line = '<li>{}</li>\n'.format(line.lstrip('-').strip())
                elif unordered_start:
                    html.write('</ul>\n')
                    unordered_start = False

                # Handle ordered lists
                if line.startswith('* '):
                    if not ordered_start:
                        html.write('<ol>\n')
                        ordered_start = True
                    line = '<li>{}</li>\n'.format(line.lstrip('*').strip())
                elif ordered_start:
                    html.write('</ol>\n')
                    ordered_start = False

                # Handle paragraphs
                if not (heading_level or unordered_start or ordered_start):
                    if not paragraph and len(line.strip()) > 0:
                        html.write('<p>\n')
                        paragraph = True
                    elif paragraph and len(line.strip()) == 0:
                        html.write('</p>\n')
                        paragraph = False
                    elif paragraph:
                        html.write('<br/>\n')

                if len(line.strip()) > 0:
                    html.write(line)

            # Close any open tags
            if unordered_start:
                html.write('</ul>\n')
            if ordered_start:
                html.write('</ol>\n')
            if paragraph:
                html.write('</p>\n')

    exit(0)
