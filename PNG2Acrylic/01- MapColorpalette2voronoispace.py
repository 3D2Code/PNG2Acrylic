import os;import time;import json;import math;import re;import random
#os.chdir('C:\\Users\\buzman.CORIOLIS-COMPOS\\Desktop\\colors\\Potrace Tester')
os.chdir('C:\\Users\\burak\\Google Drive\\Python Files\\PNG2Acrylic')

import re
from ast import literal_eval

def readsphericalsurfaceincrements():
    filename='sphericalsurfaces.txt'
    surfaceincrementlist=[]
    inputfile=open(filename,'r')
    for line in inputfile:
        templine=line.strip()
        surfaceincrementlist.append(literal_eval(templine))
    inputfile.close()
    return surfaceincrementlist
    #always assign this function to a variable, otherwise it will try to print a gigantic file on screen


#where palette is a tuple containing a bunch of (r,g,b) codes that are obtained from the color palette to be used.
def mapcolorspace2palette(palette):
    #copy the palettedef to a new list called templist
    t0=time.time()
    templist=[]
    for color in palette:
        templist.append(color)
    colormapdict={}

    inputfilename='sphericalsurfaces.txt' 
    #this is a fixed file of 1GB size that defines the pixels increments one must do in x,y,z to obtain a spherical surface with a radius of r pixels. Eachline of the text file corresponds to one r value.
    inputfile=open(inputfilename,'r')
    
    ct=0
    while ct <= 444:
#for each radius value read the spherical surface increments
        line=inputfile.readline()
        templine=line.strip()
        incrementlist=literal_eval(templine)    
        colindex=0
        while colindex< len(templist):
            color=templist[colindex]
            color_bool=False
            for increment in incrementlist:
                newvoxel_in_colormap=(color[0]+increment[0],color[1]+increment[1],color[2]+increment[2])
                if 0<=newvoxel_in_colormap[0]<=255 and 0<=newvoxel_in_colormap[1]<=255 and 0<=newvoxel_in_colormap[2]<=255:
                    if not(newvoxel_in_colormap in colormapdict):
                        colormapdict[newvoxel_in_colormap]=color
                        color_bool=True
                    else:
                        existingcolor=colormapdict[newvoxel_in_colormap]
                        existingdistance=math.sqrt((newvoxel_in_colormap[0]-existingcolor[0])**2+(newvoxel_in_colormap[1]-existingcolor[1])**2+(newvoxel_in_colormap[2]-existingcolor[2])**2)
                        newcolordistance=math.sqrt((newvoxel_in_colormap[0]-color[0])**2+(newvoxel_in_colormap[1]-color[1])**2+(newvoxel_in_colormap[2]-color[2])**2)
                        if newcolordistance<=existingdistance:
                            colormapdict[newvoxel_in_colormap]=color
                            color_bool=True
            if not(color_bool):
                templist.remove(color)
                print ('removed color  ', color, ' remaining colors in palette: ', len(templist))
                colindex=colindex-1
            colindex=colindex+1
        if len(templist)<1:
            maxcount=ct
            ct=500
            print ('max diameter of expanding spheres was  ', maxcount, ' pixels')
        ct=ct+1
    print('mapping the whole palette took ', time.time()-t0)
    return colormapdict #this returns the colormap. Always assign a variable to this otherwise it will print to screen 500MB of data.

#line below maps the palette called 'palettedef' to the colorspace (RGB cube) using a 3D voronoi space.
#newcolormapdict=mapcolorspace2palette(palettedef)

def writecolormapdictionary2file(colormapdict,filename):
#following code saves the dictionary colormapdict to a text file (result is around 500MB). 
    with open(filename,"w") as outputfile:
        for keys in colormapdict:
            tempstr=str(keys)+':'+str(colormapdict[keys])+'\n'
            x=outputfile.write(tempstr)

#a0=writecolormapdictionary2file(newcolormapdict,'ArtMarkerPaletteColorMapDict.txt')

import re
from ast import literal_eval
#following code reads a text file into a dictionary called colormapdict (result is around 500MB)
#text file is in the format (R_colorspaceloc,G_colorspaceloc, B_colorspaceloc):(R_palette,G_palette,B_palette) \n (line return for each entry) 
#the colormap dictionary is in the format of (R_colorgamut,G_colorgamut, B_colorgamut):(R_palette,G_palette,B_palette) where it maps the generic sRGB color space to the best available RGB colors on the palette based on a voronoi map partition of the color space.

def readcolormapfromfile(filename):
    colormapdict={}
    inputfile=open(filename,'r')
    for line in inputfile:
        templine=line.strip()
        stringline=re.split(':',templine)
        key0=literal_eval(stringline[0])
        val0=literal_eval(stringline[1])
        colormapdict[key0]=val0
    inputfile.close()
    return colormapdict
    #always assign this function to a variable, otherwise it will try to print a 500MB file on screen
    
#os.chdir('C:\\Users\\burak\\Google Drive\\Python Files\\PNG2Acrylic')

#colormapdict=readcolormapfromfile('mappedpalette.txt')
