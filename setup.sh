#!/bin/bash

set -ex
#python -m venv myblog-venv
#.  myblog-venv/bin/activate
pip install pelican markdown ghp-import
#pip freeze > requirements.txt

#pelican-quickstart

# Install theme
git clone git@github.com:gilsondev/pelican-clean-blog.git
pelican-themes --install pelican-clean-blog --verbose
rm -rf pelican-clean-blog
pelican-themes --list

pelican content
pelican --listen -p 4242


pelican content
ghp-import output
git push origin gh-pages
