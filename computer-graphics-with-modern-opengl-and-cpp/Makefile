.POSIX:
.SUFFIXES:
.PHONY: \
	all \
	format \
	clean

CXX=clang++
CXXFLAGS=-std=c++17 -Wall -Wextra -Wdouble-promotion -pedantic-errors
LDFLAGS=-lGL -lGLEW -lglfw

all: main

main: main.cpp
	$(CXX) -o $@ $(CXXFLAGS) $^ $(LDFLAGS)

format:
	clang-format -i *.cpp

clean:
	rm -f main
