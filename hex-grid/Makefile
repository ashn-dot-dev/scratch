.POSIX:
.SUFFIXES:
.PHONY: \
	all \
	build-desktop \
	build-web \
	clean

TARGET=hex-grid

EMCC = emcc
EMCFLAGS = \
	$(CFLAGS) \
	-sASSERTIONS -sASYNCIFY -sSINGLE_FILE=1 \
	-sUSE_GLFW=3 \
	--shell-file $(SUNDER_HOME)/lib/raylib/emscripten-shell.html

all: build-desktop build-web

build-desktop:
	SUNDER_CFLAGS="$(CFLAGS)"
	sunder-compile \
		-o $(TARGET) \
		$$($(SUNDER_HOME)/lib/raylib/raylib-config desktop --libs) \
		main.sunder

build-web:
	SUNDER_ARCH=wasm32 \
	SUNDER_HOST=emscripten \
	SUNDER_CC=$(EMCC) \
	SUNDER_CFLAGS="$(EMCFLAGS)" \
	sunder-compile \
		-o $(TARGET).html \
		$$($(SUNDER_HOME)/lib/raylib/raylib-config web --libs) \
		main.sunder

clean:
	rm -f $(TARGET) $(TARGET).html *.wasm *.o *.c
