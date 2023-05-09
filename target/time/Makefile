mkbin:
	mkdir -p bin

run: mkbin lib
	clang++ main.cpp -O3 -o bin/main ./bin/time && ./bin/main

lib: mkbin
	clang++ time.cpp -shared -g -o ./bin/time

# example afl++ instrumentation
w_afl: mkbin
	afl-clang-fast++ time.cpp -shared -g -o ./bin/time

hand: mkbin lib
	clang++ hand.cpp -std=c++17 -fsanitize=fuzzer,address -o ./bin/fuzzer ./bin/time && ./bin/fuzzer

clean:
	rm -rf bin crash-*
