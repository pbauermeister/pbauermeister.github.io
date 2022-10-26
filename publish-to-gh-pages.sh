#!/bin/bash

set -ex

pelican content
ghp-import output
git push origin gh-pages
