#!/usr/bin/env bash

#Go through all contents and cd into each directory
for f in *; do
    if [ -d ${f} ]; then
        echo "# Part Category: $f #"
        cd $f
        #If build script exists then execute it
        if [ -f build.sh ]; then
            ./build.sh
        fi
        cd ../
    fi
done
