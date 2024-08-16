# See [classfuzzgen](https://github.com/k0tran/classfuzzgen)

# DwarfFuzz

This fuzzer aims to utilize [dwarf debugging format](https://dwarfstd.org/) for fuzzing purposes

**Note: this project abandoned in favor of [cfuzz](github.com/k0tran/cfuzz)**

## Current Goals

- C++-only
- Source code required
- Dwarf info as tool to get initial information about fuzz target
- Fuzzer generation
- Based of libFuzzer
- AFL++ support

## Upcoming goals

- Language-agnostic (all information from dwarfinfo with library linkage)
- No source code required (generate extern's from dwarf info)
- Faster language for fuzzer generation (replace python)

# Project structure

**src/** - fuzzer generator

**target/** - example targets for testing. Each one of those should contain at least Makefile for building target class lib

# How to run

if needed check out [src/main.py](gen/main.py) for more info

## libFuzzer example
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

## AFL++ example

Export flags for AFL:
```bash
$ export AFL_USE_ASAN=1
```

Build class as separate lib with preferred instrumentation
```bash
$ cd target/time
$ make w_afl
$ cd ../..
```
Look at `w_afl` target in Makefile for instrumentation example


Generate the fuzzer (as in libFuzzer example)
```bash
$ python src/main.py target/time/bin/time Time target/time/time.hpp fuzzer.cpp
```

Compile it with `afl-clang++` (don't forget `c++17` flag):
```bash
$ afl-clang-fast++ fuzzer.cpp -std=c++17 -fsanitize=fuzzer -o fuzzer target/time/bin/time
```

Generate corpus (the bigger the corpus the more effective fuzzing):
```bash
$ mdkir input
$ echo 'asfojgioer' > input/example
```

Run it (for example for 60 seconds):
```bash
$ afl-fuzz -V 60 -i input/ -o output/ -- ./fuzzer
```

Crashes can be found in `output/default/crashes` and tested with `./fuzzer [path to crash]`

## Requirments

- AFL++/libFuzzer
- python elftools
