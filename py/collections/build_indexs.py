#
# Build an index with word -> list of pairs(line_number, column_number)
# Examples from 'Fluent Python' by Luciano Ramalho

import re
import collections

WORD_RE = re.compile(r'\w+')
# Our dictionary word -> list[(lno, cn),..., (lno, cn)]
# Use default dictionary so that missing items return a
# default value of []
index = collections.defaultdict(list)
filename = 'data/README.md'
if __name__ == '__main__':
    # Open the file
    with open(filename, encoding='utf-8') as fp:
        for line_no, line in enumerate(fp, 1):
            for match in WORD_RE.finditer(line):
                word = match.group()
                column_no = match.start()+1
                location = (line_no, column_no)
                # Use defaul item if item not in the dict
                index[word].append(location)
    # Print in alphabetical order
    for word in sorted(index, key=str.upper):
        print(word, index[word])
