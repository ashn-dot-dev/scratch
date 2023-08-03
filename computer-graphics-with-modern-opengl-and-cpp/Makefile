.POSIX:
.SUFFIXES:
.PHONY: \
	all \
	format \
	clean

CXX=g++
CXXFLAGS=-std=c++17 -Wall -Wextra -Wconversion -pedantic-errors
LDFLAGS=-lGL -lGLEW -lglfw

all: main

main: main.cpp mesh.cpp shader.cpp util.cpp window.cpp
	$(CXX) -o $@ $(CXXFLAGS) $^ $(LDFLAGS)

format:
	clang-format -i *.hpp *.cpp

clean:
	rm -f main
