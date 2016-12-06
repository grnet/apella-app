#!/bin/sh

help () {
    echo "Usage: $0 <target_environment>"
}

if [ -z "$1" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    help
    exit 1
fi

cmd () {
    echo --- "$@"
    "$@"
}

target_env="$1"

cmd npm install npm
cmd ./node_modules/.bin/npm install bower
cmd ./node_modules/.bin/npm install
cmd ./node_modules/.bin/bower install --allow-root
cmd ./node_modules/.bin/ember build --environment "${target_env}" --output-path dist

