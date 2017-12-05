"""
A very strange assembler for the MOS 6502 instruction set

"""
import sys
from collections import namedtuple

SourceLine = namedtuple('SourceLine', ['number', 'code'])



opcodes = {

    'adc' : {
        'imm'     : (0x69),
        'zp'      : (0x65),
        'zp x'    : (0x75),
        'abs'     : (0x6d),
        'abs x'   : (0x7d),
        'abs y'   : (0x79),
        'ind x'   : (0x61),
        'ind y'   : (0x71)
        },

    'and' : {
        'imm'     : (0x29),
        'zp'      : (0x25),
        'zp x'    : (0x35),
        'abs'     : (0x2d),
        'abs x'   : (0x3d),
        'abs y'   : (0x39),
        'ind x'   : (0x21),
        'ind y'   : (0x31)
        },

    'asl' : {
        'acc'     : (0x0a),
        'zp'      : (0x06),
        'zp x'    : (0x16),
        'abs'     : (0x0e),
        'abs x'   : (0x1e)
        },

    'bit' : {
        'zp'      : (0x24),
        'abs'     : (0x2c)
        },

    # Branch instructions
    'bpl' : {
        'rel'     : (0x10)
        },

    'bmi' : {
        'rel'     : (0x30)
        },

    'bvc' : {
        'rel'     : (0x50)
        },

    'bvs' : {
        'rel'     : (0x70)
        },

    'bcc' : {
        'rel'     : (0x90)
        },

    'bcs' : {
        'rel'     : (0xb0)
        },

    'bne' : {
        'rel'     : (0xd0)
        },

    'beq' : {
        'rel'     : (0xf0)
        },

    'brk' : {
        'imp'     : (0x00)
        },

    'cmp' : {
        'imm'     : (0xc9),
        'zp'      : (0xc5),
        'zp x'    : (0xd5),
        'abs'     : (0xcd),
        'abs x'   : (0xdd),
        'abs y'   : (0xd9),
        'ind x'   : (0xc1),
        'ind y'   : (0xd1)
        },

    'cpx' : {
        'imm'     : (0xe0),
        'zp'      : (0xe4),
        'abs'     : (0xec)
        },

    'cpy' : {
        'imm'     : (0xc0),
        'zp'      : (0xc4),
        'abs'     : (0xcc)
        },

    'dec' : {
        'zp'      : (0xc6),
        'zp x'    : (0xd6),
        'abs'     : (0xce),
        'abs x'   : (0xde)
        },

    'eor' : {
        'imm'     : (0x49),
        'zp'      : (0x45),
        'zp x'    : (0x55),
        'abs'     : (0x4d),
        'abs x'   : (0x5d),
        'abs y'   : (0x59),
        'ind x'   : (0x41),
        'ind y'   : (0x51)
        },

    'clc' : {
        'imm'     : (0x18)
        },

    'sec' : {
        'imm'     : (0x38)
        },

    'cli' : {
        'imm'     : (0x58)
        },

    'sei' : {
        'imm'     : (0x78)
        },

    'clv' : {
        'imm'     : (0xb8)
        },

    'cld' : {
        'imm'     : (0xd8)
        },

    'sed' : {
        'imm'     : (0xf8)
        },

    'inc' : {
        'zp'      : (0xe6),
        'zp x'    : (0xf6),
        'abs'     : (0xee),
        'abs x'   : (0xfe)
        },

    'jmp' : {
        'abs'     : (0x4c),
        'abs ind' : (0x6c)
        },

    'jsr' : {
        'abs'     : (0x20)
        },

    'lda' : {
        'imm'     : (0xa9),
        'zp'      : (0xa5),
        'zp x'    : (0xb5),
        'abs'     : (0xad),
        'abs x'   : (0xbd),
        'abs y'   : (0xb9),
        'ind x'   : (0xa1),
        'ind y'   : (0xb1)
        },

    'ldx' : {
        'imm'     : (0xa2),
        'zp'      : (0xa6),
        'zp y'    : (0xb6),
        'abs'     : (0xae),
        'abs y'   : (0xbe)
        },

    'ldy' : {
        'imm'     : (0xa0),
        'zp'      : (0xa4),
        'zp x'    : (0xb4),
        'abs'     : (0xac),
        'abs x'   : (0xbc)
        },

    'lsr' : {
        'acc'     : (0x4a),
        'zp'      : (0x46),
        'zp x'    : (0x56),
        'abs'     : (0x4e),
        'abs x'   : (0x5e)
        },

    'nop' : {
        'imp'     : (0xea)
        },

    'ora' : {
        'imm'     : (0x09),
        'zp'      : (0x05),
        'zp x'    : (0x15),
        'abs'     : (0x0d),
        'abs x'   : (0x1d),
        'abs y'   : (0x19),
        'ind x'   : (0x01),
        'ind y'   : (0x11)
        },

    'tax' : {
        'imp'     : (0xaa)
        },

    'txa' : {
        'imp'     : (0x8a)
        },

    'dex' : {
        'imp'     : (0xca)
        },

    'inx' : {
        'imp'     : (0xe8)
        },

    'tay' : {
        'imp'     : (0xa8)
        },

    'tya' : {
        'imp'     : (0x98)
        },

    'dey' : {
        'imp'     : (0x88)
        },

    'iny' : {
        'imp'     : (0xc8)
        },

    'rol' : {
        'imm'     : (0x2a),
        'zp'      : (0x26),
        'zp y'    : (0x36),
        'abs'     : (0x2e),
        'abs y'   : (0x3e)
        },

    'ror' : {
        'imm'     : (0x6a),
        'zp'      : (0x66),
        'zp y'    : (0x76),
        'abs'     : (0x6e),
        'abs y'   : (0x7e)
        },

    'rti' : {
        'imp'     : (0x40)
        },

    'rts' : {
        'imp'     : (0x60)
        },

    'sbc' : {
        'imm'     : (0xe9),
        'zp'      : (0xe5),
        'zp x'    : (0xf5),
        'abs'     : (0xed),
        'abs x'   : (0xfd),
        'abs y'   : (0xf9),
        'ind x'   : (0xe1),
        'ind y'   : (0xf1)
        },

    'sta' : {
        'zp'      : (0x85),
        'zp x'    : (0x95),
        'abs'     : (0x8d),
        'abs x'   : (0x9d),
        'abs y'   : (0x99),
        'ind x'   : (0x81),
        'ind y'   : (0x91)
        },

    'txs' : {
        'imp'     : (0x9a)
        },

    'tsx' : {
        'imp'     : (0xba)
        },

    'pha' : {
        'imp'     : (0x48)
        },

    'pla' : {
        'imp'     : (0x68)
        },

    'php' : {
        'imp'     : (0x08)
        },

    'plp' : {
        'imp'     : (0x28)
        },

    'stx' : {
        'zp'      : (0x86),
        'zp y'    : (0x96),
        'abs'     : (0x8e)
        },

    'sty' : {
        'zp'      : (0x84),
        'zp x'    : (0x94),
        'abs'     : (0x8c)
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
