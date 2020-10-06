#!/usr/bin/env python3
from KicadModTree import *
import csv

#Define vars for HPCE [mm] 
drill_pad = 0.7
drill_mount = 2.35
pitch = 1
annular_ring = 0.25

dim_b = {36: 25, 64: 39, 98: 56, 164: 89}
dim_c = {36: 9.15, 64: 23.15, 98: 40.15, 164: 73.15}

num_pos = [36,64,98,164]
for pos in num_pos:
    name = "HPCE_{}_female".format(pos)
    #Initial formatting
    kicad_mod = Footprint(name)
    kicad_mod.append(Text(type='reference', text='REF**', at=[0,0], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=name, at=[0,0], layer='F.Fab'))
    kicad_mod.setDescription("Female Edge Connector: {} (https://www.amphenol-icc.com/media/wysiwyg/files/drawing/10018783.pdf)".format(name))
    #Create courtyard
    kicad_mod.append(RectLine(start=[-1.85, -4.5], end=[-1.85+dim_b[pos], 4.5], layer='F.CrtYd'))
    kicad_mod.append(RectLine(start=[-1.85, -4.5], end=[-1.85+dim_b[pos], 4.5], layer='B.CrtYd'))
    for side in ['A','B']:
        for i in range(1,int(pos/2)+1):
            if side == 'A':
                #A Side Outer Row(A2,A4,A6,etc...)
                if i % 2 == 0:
                    #After first mounting position
                    if i > 10: 
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[i*pitch+2,-3.25], size=[drill_pad+(annular_ring*2),drill_pad+(annular_ring*2)],
                                drill=0.7, layers=Pad.LAYERS_THT))
                    #Before first mounting position
                    else: 
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[i,-3.25], size=[1.2,1.2], drill=0.7, layers=Pad.LAYERS_THT))
                #A Side Middle Row(A1,A3,A5,etc...)
                else:
                    #For A1 Only
                    if i == 1:
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                            at=[i,-1.25], size=[1.2,1.2], drill=0.7, layers=Pad.LAYERS_THT))
                    else:    
                        #After first mounting position
                        if i > 11: 
                            kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                at=[i+2,-1.25], size=[1.2,1.2], drill=0.7, layers=Pad.LAYERS_THT))
                        #Before first mounting position
                        else: 
                            kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                at=[i,-1.25], size=[1.2,1.2], drill=0.7, layers=Pad.LAYERS_THT))
            else:
                #B Side Outer Row (B2,B4,B6,etc...)
                if i % 2 == 0:
                    #After first mounting position
                    if i > 10: 
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[i+2,3.25], size=[1.2,1.2], drill=0.7, layers=Pad.LAYERS_THT))
                    #Before first mounting position
                    else: 
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[i,3.25], size=[1.2,1.2], drill=0.7, layers=Pad.LAYERS_THT))
                #B Side Middle Row(B1,B3,B5,etc...)
                else:
                    #After first mounting position
                    if i > 11: 
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[i+2,1.25], size=[1.2,1.2], drill=0.7, layers=Pad.LAYERS_THT))
                    #Before first mounting position
                    else: 
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[i,1.25], size=[1.2,1.2], drill=0.7, layers=Pad.LAYERS_THT))
    #Add mounting holes
    kicad_mod.append(Pad(at=[11*pitch+1.65,0],type=Pad.TYPE_NPTH,layers=Pad.LAYERS_NPTH,
        shape=Pad.SHAPE_CIRCLE,size=drill_mount,drill=drill_mount))
    kicad_mod.append(Pad(at=[11*pitch+1.65+dim_c[pos],0],type=Pad.TYPE_NPTH,layers=Pad.LAYERS_NPTH,
        shape=Pad.SHAPE_CIRCLE,size=drill_mount,drill=drill_mount))
    #Export .kicad_mod file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{}.kicad_mod'.format(name),timestamp=0)

