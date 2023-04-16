# DwarfFuzz

This fuzzer aims to utilize [dwarf debugging format](https://dwarfstd.org/) for fuzzing purposes

## Current Goals

- C++-only
- Source code required
- Dwarf info as tool to get initial information about fuzz target
- Fuzzer generation
- Based of libFuzzer

## Upcoming goals

- Language-agnostic (all information from dwarfinfo with library linkage)
- No source code required (generate extern's from dwarf info)
- AFL/AFL++ support
- Faster language for fuzzer generation (replace python)

# Project structure

**gen/** - fuzzer generator

**target/** - example targets for testing. Each one of those should contain at least Makefile for building target class lib

# How to run

Look up the usage:
```bash
python gen/main.py --help
```

Check out [gen/main.py](gen/main.py) for more info