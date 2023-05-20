.POSIX:
.SUFFIXES:
.PHONY: \
	all \
	clean

ASSIGNMENTS = \
	assignment-1 \
	assignment-2 \
	assignment-3

all: $(ASSIGNMENTS)

assignment-1: assignment-1.sunder
	SUNDER_CFLAGS="$$(sdl2-config --cflags)" \
	sunder-compile -o $@ -loat $$(sdl2-config --libs) -lSDL2_image -lSDL2_mixer -lSDL2_ttf $^

assignment-2: assignment-2.sunder
	SUNDER_CFLAGS="$$(sdl2-config --cflags)" \
	sunder-compile -o $@ -loat $$(sdl2-config --libs) -lSDL2_image -lSDL2_mixer -lSDL2_ttf $^

assignment-3: assignment-3.sunder
	SUNDER_CFLAGS="$$(sdl2-config --cflags)" \
	sunder-compile -o $@ -loat $$(sdl2-config --libs) -lSDL2_image -lSDL2_mixer -lSDL2_ttf $^

clean:
	rm -f $(ASSIGNMENTS) *.o *.c
