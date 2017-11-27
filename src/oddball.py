"""
A very strange assembler for the MOS 6502 instruction set

"""
import sys
from collections import namedtuple

SourceLine = namedtuple('SourceLine', ['number', 'code'])

opcodes = {

    'adc' :

    }

class Block(object):
    """Organize blocks of source code for assembling

    Args:
      offset (int): Absolute offset address
      source (list): List of tuples, each contains a line number and instruction

    """
    def __init__(self, offset, source):
        self.offset = offset
        self.source = source

        self._symbols = dict()
        self._code = None
        self._bytes = 0

    def __len__(self):
        return self._bytes

    def assemble(self):
        pass

    def _first_pass(self):
        pass

    def _second_pass(self):
        pass



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

def extract_code(filename):
    """Extracts blocks of source code delineated by .org directives

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
            # Peel off the leading '$' from the source file
            offset = int(offset[1:], 16)
            blocks[offset] = list()
        # ...otherwise this line throws a NameError
        else:
            blocks[offset].append(line)
    return [Block(offset, blocks[offset]) for offset in sorted(blocks.keys())]

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

def main(args):
    blocks = extract_code('../roms/test.rom')

if __name__ == '__main__':
    sys.exit(main(sys.argv))
