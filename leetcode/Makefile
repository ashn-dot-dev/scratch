.POSIX:
.SUFFIXES:
.PHONY: \
	all
	format \
	clean

CXXFLAGS_BASE=-std=c++20 -Wall -Wextra -Wpedantic
CXXFLAGS_DBG=$(CXXFLAGS_BASE) -O0 -g
CXXFLAGS_REL=$(CXXFLAGS_BASE) -Os

SANITIZE=-fsanitize=address,leak,undefined

CXX=clang++
CXXFLAGS=$(CXXFLAGS_REL)

all: \
	problem-0001-two-sum.out \
	problem-0003-longest-substring-without-repeating-characters.out \
	problem-0004-median-of-two-sorted-arrays.out \
	problem-0009-palindrome-number.out \
	problem-0036-valid-sudoku.out \
	problem-0049-group-anagrams.out

format:
	clang-format -i *.cpp

clean:
	rm -f *.out

.SUFFIXES: .cpp .out
.cpp.out:
	$(CXX) -o $@ $(CXXFLAGS) $<
