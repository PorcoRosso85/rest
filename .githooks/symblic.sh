#!/bin/bash

# this script makes files which are same directory symbolic linked to the file in the .git/hooks directory
# if there are files with the same name in the .git/hooks directory, they will be overwritten

for file in $(ls ./.githooks); do
    if [ -f "$file" ]; then
        ln -sf "$(pwd)/$file" ".git/hooks/$file"
    fi
done
