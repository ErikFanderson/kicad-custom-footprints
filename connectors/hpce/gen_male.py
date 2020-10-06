#!/usr/bin/env python3
from KicadModTree import *
import csv

#####################################################################
##                            Variables                            ##
#####################################################################
#Define vars for HPCE [mm] 
pitch = 1
edge_padding = 0.65
pad_x = 0.70
pad_y = 4.20
pad_y_special = 3.20
arc_y = 8.40
top_pad_y = 5.60
chamfer = 1.40
gap = 1.9
edge_to_mid_gap = 12.15

dim_b = {36: 25, 64: 39, 98: 56, 164: 89}
dim_c = {36: 9.15, 64: 23.15, 98: 40.15, 164: 73.15}
dim_g = {36: 8.15, 64: 22.15, 98: 39.15, 164: 72.15}
pin_f = {36: 'B17', 64: 'B31', 98: 'B48', 164: 'B81'}

#Centering Offset
x_o = -pitch + edge_padding
y_o = 0

#####################################################################
##                          Generate FP                            ##
#####################################################################
num_pos = [36,64,98,164]
for pos in num_pos:
    name = "HPCE_{}_male".format(pos)
    #Initial formatting
    kicad_mod = Footprint(name)
    kicad_mod.append(Text(type='reference', text='REF**', at=[0,0], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=name, at=[0,0], layer='F.Fab'))
    kicad_mod.setDescription("Male Edge Connector: {} (https://www.amphenol-icc.com/media/wysiwyg/files/drawing/10018783.pdf)".format(name))
    for side in ['A','B']:
        for i in range(1,int(pos/2)+1):
            if side == 'A':
                if i == 1:
                    kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[(i*pitch)+x_o,-((pad_y-pad_y_special)/2)-y_o], size=[pad_x,pad_y_special],layers=['B.Cu','B.Mask']))
                else:
                    if i > 11: 
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                            at=[(i*pitch+2)+x_o,0-y_o], size=[pad_x,pad_y],layers=['B.Cu','B.Mask']))
                    else:
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                            at=[(i*pitch)+x_o,0-y_o], size=[pad_x,pad_y],layers=['B.Cu','B.Mask']))
            else:
                if (side + str(i)) == pin_f[pos]:
                    kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[(i*pitch+2)+x_o,-((pad_y-pad_y_special)/2)-y_o], size=[pad_x,pad_y_special],layers=['F.Cu','F.Mask']))
                else:
                    if i > 11: 
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                            at=[(i*pitch+2)+x_o,0-y_o], size=[pad_x,pad_y],layers=['F.Cu','F.Mask']))
                    else:
                        kicad_mod.append(Pad(number=side+str(i), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                            at=[(i*pitch)+x_o,0-y_o], size=[pad_x,pad_y],layers=['F.Cu','F.Mask']))
    #Add sides
    kicad_mod.append(Line(start=[(pitch-edge_padding)+x_o,(pad_y/2+chamfer)-y_o],
        end=[(pitch-edge_padding)+x_o,(pad_y/2+chamfer-arc_y)-y_o],width=0.10,layer='Dwgs.User'))
    kicad_mod.append(Line(start=[(pitch-edge_padding+edge_to_mid_gap+dim_g[pos])+x_o,(pad_y/2+chamfer)-y_o],
        end=[(pitch-edge_padding+edge_to_mid_gap+dim_g[pos])+x_o,(pad_y/2+chamfer-arc_y)-y_o],width=0.10,layer='Dwgs.User'))
    #Add bottom edge of chamfer
    kicad_mod.append(Line(start=[(pitch-edge_padding)+x_o,(pad_y/2+chamfer)-y_o],
        end=[(pitch-edge_padding+edge_to_mid_gap-gap/2)+x_o,(pad_y/2+chamfer)-y_o],width=0.10,layer='Dwgs.User'))
    kicad_mod.append(Line(start=[(pitch-edge_padding+edge_to_mid_gap+gap/2)+x_o,(pad_y/2+chamfer)-y_o],
        end=[(pitch-edge_padding+dim_g[pos]+edge_to_mid_gap)+x_o,(pad_y/2+chamfer)-y_o],width=0.10,layer='Dwgs.User'))
    #Add middle cutout
    kicad_mod.append(Arc(center=[(11*pitch+1.5)+x_o,-(arc_y-top_pad_y+(pad_y/2)-gap/2)-y_o],
        start=[(11*pitch+gap/2+1.5)+x_o,-(arc_y-top_pad_y+(pad_y/2)-gap/2)-y_o],
        angle=-180,width=0.10,layer='Dwgs.User'))
    kicad_mod.append(Line(start=[(pitch-edge_padding+edge_to_mid_gap-gap/2)+x_o,(pad_y/2+chamfer)-y_o],
        end=[(pitch-edge_padding+edge_to_mid_gap-gap/2)+x_o,(pad_y/2+chamfer-arc_y+gap/2)-y_o],width=0.10,layer='Dwgs.User'))
    kicad_mod.append(Line(start=[(pitch-edge_padding+edge_to_mid_gap+gap/2)+x_o,(pad_y/2+chamfer)-y_o],
        end=[(pitch-edge_padding+edge_to_mid_gap+gap/2)+x_o,(pad_y/2+chamfer-arc_y+gap/2)-y_o],width=0.10,layer='Dwgs.User'))
    #Export .kicad_mod file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{}.kicad_mod'.format(name),timestamp=0)

