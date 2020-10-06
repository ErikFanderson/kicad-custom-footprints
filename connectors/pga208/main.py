#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Erik Anderson
# Email: erik.francis.anderson@gmail.com
# Date: 10/06/2020
"""Docstring for module main"""

# Imports - standard library
import csv
import re

# Imports - 3rd party packages
from KicadModTree import *

# Imports - local source

if __name__ == '__main__':
    # Dimensions from datasheet (units in mm) - based off 17x17 footprint
    # Origin at LL corner of footprint
    A = 58.27 
    B = 48.51 
    C = 40.64 
    D = 52.71 
    pad_offset_x = 3.94 
    pad_offset_y = 3.38 
    drill_size = [0.81, 0.81]
    pad_size = [0.86, 0.86]

    # Initialize footprint (units in mils)
    name = "PGA208"
    kicad_mod = Footprint(name)
    kicad_mod.append(
        Text(type='reference', text='REF**', at=[D/2, -(A+1.27)], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=name, at=[0, 0], layer='F.Fab'))
    kicad_mod.setDescription(
        f"PGA208 socket from Aries (Mfr: 208-PRS17017-12)")

    # silkscreen outline 
    kicad_mod.append(RectLine(start=[0, -A], end=[D, 0], layer='F.SilkS', width=0.5))

    # Build array (17x17 w/ middle cutout)
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "R", "T", "U"]
    for row, letter in enumerate(letters):
        for col in range(17): 
            if letter in ["E", "F", "G", "H", "J", "K", "L", "M", "N"] and col > 3 and col < 13:
                pass
            else:
                x = (2.54 * (col)) + pad_offset_x 
                y = (2.54 * (row)) + pad_offset_y
                kicad_mod.append(
                    Pad(number=f"{letter}{col+1}",
                        type=Pad.TYPE_THT,
                        shape=Pad.SHAPE_CIRCLE,
                        at=[x, -y],
                        size=pad_size,
                        drill=drill_size,
                        layers=["*.Cu", "*.Mask"]))

    # Output kicad file
    fh = KicadFileHandler(kicad_mod)
    fh.writeFile(f"{name}.kicad_mod")
