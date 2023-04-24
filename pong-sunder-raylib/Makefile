.POSIX:
.SUFFIXES:
.PHONY: \
	all \
	build \
	clean

TARGET=pong

all: build

build:
	sunder-compile \
		-o $(TARGET) \
		-lraylib -lGL -lm -lpthread -ldl -lrt -lX11 \
		main.sunder

clean:
	rm -f $(TARGET) *.out *.o *.c
