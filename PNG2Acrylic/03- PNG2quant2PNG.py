import os;import time;import json;import math;import re;import random
os.chdir('C:\\Users\\burak\\Google Drive\\Python Files\\PNG2Acrylic')

import PIL
from PIL import Image
import re
from ast import literal_eval

#palettedef=((0,0,0),(204,0,166),(236,175,237),(123,125,146),(33,33,34),(197,161,127),(186,176,85),(178,210,80),(245,242,199),(119,196,245),(166,233,248),(233,17,140),(250,218,157),(253,176,159),(223,183,60),(255,255,255))
#this is the palette for the Art Marker Alcohol Ink on Glossy Photo Paper

palettedef=((0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255))
#this is the palette for WRGBCMYK colors

exec(open("01- MapColorpalette2voronoispace.py").read())

#colormapdict=paletteread('mappedpalette.txt')
colormapdict=mapcolorspace2palette(palettedef)
inputimagefilename='Foto.jpg'
filenamestem=re.split('\.',inputimagefilename)[0]

firstimage=Image.open(inputimagefilename)
inputimage=firstimage.convert(mode='RGB',dither=None)
inputimage.show()

image_width,image_height=inputimage.size
image_mode=inputimage.mode

sourcepixelmap=inputimage.load()

quant_primary_image=Image.new(image_mode,inputimage.size)
quant_secondary_image=Image.new(image_mode,inputimage.size)
quant_primary_pixelmap=quant_primary_image.load()
quant_secondary_pixelmap=quant_secondary_image.load()

for j in range(image_height):
    for i in range(image_width):
        sourcecolor=sourcepixelmap[i,j]
        primary_quant_color=colormapdict[sourcecolor]
        quant_primary_pixelmap[i,j]=primary_quant_color
        
        veclength=math.sqrt((sourcecolor[0]-primary_quant_color[0])**2+(sourcecolor[1]-primary_quant_color[1])**2+(sourcecolor[2]-primary_quant_color[2])**2)
        if veclength<=0.5:
            secondary_quant_color=primary_quant_color
            quant_secondary_pixelmap[i,j]=secondary_quant_color
        else:
            unitvec=( (sourcecolor[0]-primary_quant_color[0])/veclength,(sourcecolor[1]-primary_quant_color[1])/veclength, (sourcecolor[2]-primary_quant_color[2])/veclength)
            temppixel_list=[]
            for kk in range(255):
                temppixel=(int(sourcecolor[0]+kk*unitvec[0]),int(sourcecolor[1]+kk*unitvec[1]),int(sourcecolor[2]+kk*unitvec[2]))
                if not(0<=temppixel[0]<=255 and 0<=temppixel[1]<=255 and 0<=temppixel[2]<=255):
                    secondary_quant_color=primary_quant_color
                    quant_secondary_pixelmap[i,j]=secondary_quant_color
                    kk=300
                elif  not(temppixel in temppixel_list):
                    tempcolor=colormapdict[temppixel]
                    if tempcolor==primary_quant_color:
                        temppixel_list.append(temppixel)
                    else:
                        secondary_quant_color=tempcolor
                        quant_secondary_pixelmap[i,j]=secondary_quant_color
                        kk=300

firstimage.close()

quant_primary_image.show()
quant_primary_image_filename=filenamestem+'_quant_primary.png'
quant_primary_image.save(quant_primary_image_filename)
quant_primary_image.close()

quant_secondary_image.show()
quant_secondary_image_filename=filenamestem+'_quant_secondary.png'
quant_secondary_image.save(quant_secondary_image_filename)
quant_secondary_image.close()