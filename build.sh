#!/bin/sh

find $(dirname "${0}") -mindepth 2 -maxdepth 2 -name 'build.sh' -exec {} \;
