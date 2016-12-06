#!/bin/sh

build_env="$1"

cmd() {
    echo --- "$@"
    "$@"
}

cmd cd ui/
cmd exec ./build_ui.sh "${build_env}"
