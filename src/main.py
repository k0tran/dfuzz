# Class fuzzer generator
# with v0.1 you can check out v0.1 generation example (target/time/hand.cpp)
#
# Usage:
# python src/main.py compiled_lib class_name class_header_file
# Lib should be compiled with dwarf info (-g flag)

VERSION = '0.1'

import argparse
from elftools.elf.elffile import ELFFile
from pathlib import Path

from classdata import parse


# Find right Compile Unit
def find_cu(filename, class_name):
    with open(filename, 'rb') as f:
        elf = ELFFile(f)

        if not elf.has_dwarf_info():
            print("Dwarf info not found")
            exit(1)

        dinfo = elf.get_dwarf_info()
        cus = [cu for cu in dinfo.iter_CUs()] # bc it's generator
 
        # if there's only one CU
        if len(cus) == 1:
            return cus[0]
        
        # Found several several CU's
        print('Found several CU\'s, choose the correct one')
        for i in range(len(cus)):
            print('//', str(i) + ')', Path(cus[i].get_top_DIE().get_full_path()).as_posix())

        i = int(input())
        if i >= len(cus):
            return None
        return cus[i]


def main(lib, class_name, class_header, out):
    cu = find_cu(lib, class_name)
    if cu is None:
        print('Incorrect CU ID')
        return
    data = parse(cu, class_name)
    f = data.fuzzer(class_header)
    with open(out, 'w') as o:
        o.write(f)


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(
        prog='Class Fuzzer Generator',
        description='generate class fuzzer',
        epilog='v{}'.format(VERSION)
    )
    
    parser.add_argument('lib_file')
    parser.add_argument('class_name')
    parser.add_argument('class_header')
    parser.add_argument('output')

    args = parser.parse_args()
    main(args.lib_file, args.class_name, args.class_header, args.output)