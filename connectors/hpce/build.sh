#!/bin/bash

#Generate kicad_mod files
/usr/bin/env python3 gen_male.py
/usr/bin/env python3 gen_female.py

#Move all generated files into Edge_Connectors library
for file in *.kicad_mod; do
    mv $file ../../Edge_Connectors.pretty
done
