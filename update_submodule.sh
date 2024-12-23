#!/usr/bin/env bash

git submodule update --remote

git submodule foreach --recursive '
  git checkout master
  git fetch origin
  git rebase origin/master
'