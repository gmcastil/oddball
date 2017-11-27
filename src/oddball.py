"""
A very strange assembler for the MOS 6502 instruction set

"""
import sys
from collections import namedtuple

SourceLine = namedtuple('SourceLine', ['number', 'code'])

def stripped(filename):
    """Generates a sequence of source code lines without comments or whitespace

    Args:
      lines (iter) - Iterable of lines of source, probably from an .asm file

    Yields:
      tuple - Line numbers and instructions or assembler directives

    """
    with open(filename, 'r') as lines:
        for number, line in enumerate(lines, 1):
            # Only deal with lowercase values
            line = line.lower().strip()
            # Eliminate comment lines
            if line.startswith(';'):
                continue
            # Eliminate whitespace lines
            if not line:
                continue
            # Eliminate any trailing comments and whitespace before yielding
            if ';' in line:
                comment_index = line.find(';')
                code = line[0:comment_index].strip()
            else:
                code = line.strip()
            line = SourceLine(number, code)
            yield line

def code_blocks(filename):
    """Extracts blocks of source code separated by and .org directive

    Args:
      filename (str): Source code filename

    Returns
      dict - Keys are derived from origin directives. Values are lists of
             instructions to be placed there

    """
    source_code = stripped(filename)
    blocks = dict()
    for line in source_code:
        # This requires that an .org directive appear before any code...
        if is_origin(line.code):
            directive, offset = line.code.split()
            blocks[offset] = []
        # ...otherwise this line throws a NameError
        else:
            blocks[offset].append(line)
    return blocks

def is_origin(line):
    """Returns True if line is a valid origin directive

    Args:
      line (str): Line of valid source code

    Returns:
      bool

    """
    status = False
    directive = 'org'
    if line.startswith('.' + directive):
        status = True
    return status

def first_pass(code, pc=0):
    """Builds a symbol table containing label names and addresses

    Args:
      code (iter) - Iterable of lines of source code
      pc (int) - Program counter initial value

    Returns:
      dict - Labels mapped to absolute addresses

    """
    symbol_table = dict()
    for address, line in enumerate(code, pc):
        if len(line.code.split(':')) > 1:
            label = line.code.split(':')[0]
            symbol_table[label] = address
    return symbol_table

def main(args):
    blocks = code_blocks('../roms/test.rom')



if __name__ == '__main__':
    sys.exit(main(sys.argv))
