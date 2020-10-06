#!/usr/bin/env bash

# High Power Card Edge Connectors 
python3 hpce/gen_male.py
python3 hpce/gen_female.py
mv *.kicad_mod zz_hpce.pretty/

# Sockets 
python3 pga208/main.py
mv *.kicad_mod zz_sockets.pretty/
