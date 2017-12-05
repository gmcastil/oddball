"""
A very strange assembler for the MOS 6502 instruction set

"""
import sys
from collections import namedtuple

SourceLine = namedtuple('SourceLine', ['number', 'code'])



opcodes = {

    'adc' : {
        'imm'   : (0x69),
        'zp'    : (0x65),
        'zp x'  : (0x75),
        'abs'   : (0x6d),
        'abs x' : (0x7d),
        'abs y' : (0x79),
        'ind x' : (0x61),
        'ind y' : (0x71)
        },

    'and' : {
        'imm'   : (0x29),
        'zp'    : (0x25),
        'zp x'  : (0x35),
        'abs'   : (0x2d),
        'abs x' : (0x3d),
        'abs y' : (0x39),
        'ind x' : (0x21),
        'ind y' : (0x31)
        },

    'asl' : {
        'acc'   : (0x0a),
        'zp'    : (0x06),
        'zp x'  : (0x16),
        'abs'   : (0x0e),
        'abs x' : (0x1e)
        },

    'bit' : {
        'zp'    : (0x24),
        'abs'   : (0x2c)
        },

    # Branch instructions
    'bpl' : {
        'rel'   : (0x10)
        },

    'bmi' : {
        'rel'   : (0x30)
        },

    'bvc' : {
        'rel'   : (0x50)
        },

    'bvs' : {
        'rel'   : (0x70)
        },

    'bcc' : {
        'rel'   : (0x90)
        },

    'bcs' : {
        'rel'   : (0xb0)
        },

    'bne' : {
        'rel'   : (0xd0)
        },

    'beq' : {
        'rel'   : (0xf0)
        },

    'brk' : {
        'imp'   : (0x00)
        },

    'cmp' : {
        'imm'   : (0xc9),
        'zp'    : (0xc5),
        'zp x'  : (0xd5),
        'abs'   : (0xcd),
        'abs x' : (0xdd),
        'abs y' : (0xd9),
        'ind x' : (0xc1),
        'ind y' : (0xd1)
        },

    'cpx' : {
        'imm'   : (0xe0),
        'zp'    : (0xe4),
        'abs'   : (0xec)
        },

    'cpy' : {
        'imm'   : (0xc0),
        'zp'    : (0xc4),
        'abs'   : (0xcc)
        },

    'dec' : {
        'zp'    : (0xc6),
        'zp x'  : (0xd6),
        'abs'   : (0xce),
        'abs x' : (0xde)
        },

    'eor' : {
        'imm'   : (0x49),
        'zp'    : (0x45),
        'zp x'  : (0x55),
        'abs'   : (0x4d),
        'abs x' : (0x5d),
        'abs y' : (0x59),
        'ind x' : (0x41),
        'ind y' : (0x51)
        },

    'clc' : {
        'imm'   : (0x18)
        },

    'sec' : {
        'imm'   : (0x38)
        },

    'cli' : {
        'imm'   : (0x58)
        },

    'sei' : {
        'imm'   : (0x78)
        },

    'clv' : {
        'imm'   : (0xb8)
        },

    'cld' : {
        'imm'   : (0xd8)
        },

    'sed' : {
        'imm'   : (0xf8)
        },

    }


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


def parse_addr_mode(opcode, operands):
    """

    """


def stripped(filename):
    """Generates a sequence of source code lines without comments or whitespace

    Args:
      filename (str) - Filename to strip of whitespace and comments

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
