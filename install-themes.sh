#!/bin/bash

set -e

if [ ! -d pelican-themes ]; then
    git clone --recursive git@github.com:getpelican/pelican-themes.git
fi

for d in $(find pelican-themes -type d -maxdepth 1); do
    echo
    echo "Installing: $d"
    pelican-themes --install $d --verbose
done

pelican-themes --list | sort
