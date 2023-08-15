.POSIX:
.SUFFIXES:
.PHONY: \
	all
	format \
	clean

CXXFLAGS_BASE=-std=c++20 -Wall -Wextra -Wpedantic
CXXFLAGS_DBG=$(CXXXFLAGS_BASE) -O0 -g -fsanitize=address,leak,undefined
CXXFLAGS_REL=$(CXXXFLAGS_BASE) -Os

CXX=g++
CXXFLAGS=$(CXXFLAGS_REL)

all: \
	problem-36-valid-sudoku.out

format:
	clang-format -i *.cpp

clean:
	rm -f *.out

.SUFFIXES: .cpp .out
.cpp.out:
	$(CXX) -o $@ $(CXXFLAGS) $<
