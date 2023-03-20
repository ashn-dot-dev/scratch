#!/bin/sh
set -eu

INIT=false

for _ in "$@"; do
case "$1" in
    -i|--init)
        INIT=true
        ;;
    *)
        1>&2 echo "error: unexpected argument '$1'"
        exit 1
        ;;
esac
done

if eval "${INIT}"; then
    if [ ! -d raylib ]; then
        git clone https://github.com/ashn-dot-dev/raylib.git raylib
    fi
    (cd raylib && git fetch origin && git checkout 4.5.0 && cd src && make PLATFORM=PLATFORM_DESKTOP)

    if [ ! -d raylib-sunder ]; then
        git clone https://github.com/ashn-dot-dev/raylib-sunder.git raylib-sunder
    fi
    (cd raylib-sunder && git pull)
fi

set -x
export SUNDER_BACKEND=C
sunder-compile \
    -o pong \
    -Lraylib/src -lraylib -lGL -lm -lpthread -ldl -lrt -lX11 \
    main.sunder
