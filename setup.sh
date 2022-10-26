#!/bin/bash

set -ex
#python -m venv myblog-venv
#.  myblog-venv/bin/activate
pip install pelican markdown ghp-import
#pip freeze > requirements.txt

#pelican-quickstart

# Install theme
./install-themes.sh
./install-plugins.sh
pip3 install -r pelican-plugins/disqus_static/requirements.txt

pelican-themes --list
pelican content
pelican --listen -p 4242
