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

**src/** - fuzzer generator

**target/** - example targets for testing. Each one of those should contain at least Makefile for building target class lib

# How to run - example

First you need to build class as separate lib:
```bash
$ cd target/time
$ make lib
$ cd ../..
```

Second generate the fuzzer:
```bash
$ python src/main.py target/time/bin/time Time target/time/time.hpp fuzzer.cpp
```

Compile it with preferred libFuzzer flags (don't forget `c++17`):
```bash
$ clang++ fuzzer.cpp -std=c++17 -fsanitize=fuzzer,address -o fuzzer target/time/bin/time
```

Last but not the least: run the fuzzer!
```bash
$ ./fuzzer
```

Check out [src/main.py](gen/main.py) for more info

