"""
A very oddball assembler for the MOS 6502 instruction set

Unlike most assemblers which generate machine code for a given architecture,
this one generates memory initialization files (.mif) used for initial
configuration of Xilinx block memories.  The primary use case is to create
inputs to RTL simulations from 6502 assembly language source code and optionally
provided memory maps containing additional data to place in the final memory
initialization file.

It accepts .asm text of the following format:

         .directive     operands
label:   instr          operands       ; comments

The only supported directive is .org, which sets the current origin to a new
value.  This is used to set the program counter during assembly.  For example,
.org $8000 would instruct the assembler to start placing code at address $8000.
At least one instance of this directive should be used to indicate where to
begin placing instructions.

Since this use case is rather strange, there are a couple things to keep in
mind:

* The 'assembled' output will always be 64KB in size, since that is the size of
  the 6502 address space.
* All non-program bytes will be populated with NOP opcodes
* Since the purpose of the output is to simulate the 6502 address space,
  additional bytes will appear in the output, notably the address of the reset
  vector and interrupt handling routines in addresses $fffa through $ffff

Map Files:

If additional data are desired to be placed in memory, a .map file of the
following format can be provided as well:

$addr: $data

Where $addr is a string representing a 16-bit hex value and $data a string
representing an 8-bit hex value.  Here is an example:

$9000: $33
$9001: $ff

This would place the value $33 at address $9000 and $ff at address $9001.  Since
data placement occurs after assembly, it is possible to overwrite machine code
with data in memory.  No checking for this is done though.

Usage:

  asm6502 [options] [file]

Options:

  -c, --coe-only    Generates the interim coefficients file instead of a
                    .mif file.  Possibly useful for manually hacking of source
                    code.
  -m, --with-map    Use this file to place additional data into memory
  -o, --output      Output filename to use (optional).  Default is to use the
                    input filename with .mif

Development:

  - Iterate over stripped out source code containing only code or directives
  - Break source file up into blocks delineated by .org directives
  - Return a dictionary containing the origin addresses (keys) and code
    blocks (values)

"""
import pdb
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
