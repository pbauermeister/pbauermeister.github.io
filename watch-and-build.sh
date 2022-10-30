#!/bin/bash
set -ex

pelican content
while true; do
    inotifywait -e modify content/*
    pelican content
done
