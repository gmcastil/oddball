oddball - a very strange 6502 assembler
=======================================

Oddball is an assembler for the MOS Technology 6502 microprocessor.  Instead of
generating raw machine code intended to be run on the actual hardware, Oddball
produces memory maps that are intended to be used by a simulator.

Purpose
--------

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
that there was an obviously better way.

Notes
-----

Oddball parses assembly language of the following form:

```asm
          .org   $8000

label:    lda    $9000        ;; comment text
          clc
          lda    #$01
```

Usage
-----
