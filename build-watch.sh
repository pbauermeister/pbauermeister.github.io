#!/bin/sh
set -ex

pelican content
while true; do
    # apt install inotify-tools
    inotifywait -e modify content/*

    pelican content
done
