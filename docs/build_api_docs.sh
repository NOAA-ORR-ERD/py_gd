#!/bin/sh

# build API docs
# This script runs the sphinx-apidoc command with a few flags.

sphinx-apidoc --force --no-toc --module-first -o api ../py_gd/ ../py_gd/test/


