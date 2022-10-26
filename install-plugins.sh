#!/bin/bash

set -e

if [ ! -d pelican-plugins ]; then
    git clone --recursive git@github.com:getpelican/pelican-plugins.git
fi
