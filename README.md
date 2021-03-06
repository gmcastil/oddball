# Oddball - A very strange 6502 assembler

Oddball is an assembler for the MOS Technology 6502 microprocessor.  Instead of
generating raw machine code intended to be run on the actual hardware, Oddball
produces memory maps that are intended to be used by a simulator.

## Purpose

Recently, I've been developing a hardware model of the MOS Technology 6502
microprocessor in Verilog, targeting a Xilinx 7-Series field-programmable gate
array (FPGA). To simulate the design, I use a 64KB block memory generated by the
Xilinx Vivado Design Suite and then use the block memory behavioral model, my
6502 core, and a testbench to drive the whole thing. Optionally, the initial
contents of the block memory can be provided to Vivado when the IP is generated
through a coefficients (.coe) file. The tool then converts the coefficients file
to a memory initialization file (.mif) for simulation.  See [Xilinx
PG058](https://www.xilinx.com/support/documentation/ip_documentation/blk_mem_gen/v8_3/pg058-blk-mem-gen.pdf)
for more details about the block memory generator and the .coe and .mif file
formats.

I had originally been creating these manually, using some simple Python scripts
to generate 64KB .coe files filled with NOP instructions, and then hand placing
instructions and data. Inefficient and error prone to say the least. As the
number of addressing modes I implemented began to increase, it became apparent
that there was an obviously better way.  So naturally, I realized I should just
write my own assembler.

## Notes

Oddball parses assembly language of the following form:

```assembly
;; Commented text here

          .org   $8000

label:    lda    $9000        ;; More comment text
          clc
          lda    #$01
```

Currently, the only supported assembler directive is `.org` which sets the
current origin to a new value.  This is used to set the program counter during
assembly. For example, the previous code snippet would instruct the assembler to
start placing code at address $8000.  At least one instance of this directive is
required to indicate where to begin placing opcodes, data, and addresses.  If
more than one occurrence of `.org` is found in the source code, the assembler
will treat the instructions following each instance separately.

Since this is a strange use case, there are a couple of additional caveats:

* The assembled output will always be 64KB in size, since that is the size of
  the 6502 address space
* All non-program bytes will be populated with NOP (`0xEA`) opcodes
* Because the intent of the output products is to verify hardware behavior, no
  support for macros exists.

An important detail here regarding labels - all relative branch instructions
must be contained within the same code block defined by a `.org` directive.
This, for example, is not allowed

```assembly

          ;; First code block

          .org   $8000

label1:   lda    #$01
          clc
          lda    #$01
          bne    label1

          ;; Second code block

          .org   $9000
          lda    #$01
          clc
          lda    #$01
          bcc    label1
```

Since each block of code is treated independently, this would cause an error
since that particular label is not defined.  If this turns out to be a problem,
I'll probably have to rewrite some portion of the assembler.

If additional data are desired to be place in memory, a `.map` file of the
following format can be provided as well:

    # Comments here
    $9000      $33
    $9001      $ff          # Or comments can go here too

This would place the value $33 and $ff at addresses $9000 and $9001
respectively.  Depending upon how annoying I find maintaining two different
source files, I may implement some additional directives in the future.

## Usage

Oddball was developed on Python 3.6 and will not run on earlier versions (it
uses a lot of fstrings).  To run from a command prompt, type:

    oddball [options] [file]

where `file` is your input 6502 assembly source code.  Some supported options are:

    -c, --coe-only      Generates the interim coefficients file instead of a .mif
                        file.  Possibly useful for manually hacking of source code.
    -m, --with-map      Use this file to place additional data into memory
    -o, --output        Output filename to use (optional).  Default is to use the
                        input filename with .mif.
    -q, --quiet         Suppress output

## Tests

To help development, I've added a small test suite - I don't know what the code
coverage will be, but I'm going to try to make sure that I test label and branch
handling, and that addressing modes are properly decoded.  To run the test
suite, from the project directory, just run the following:

```bash

$ python3 -m unittest

```
