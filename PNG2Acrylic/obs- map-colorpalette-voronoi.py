import os;import time;import json;import math;import re;import random
#os.chdir('C:\\Users\\buzman.CORIOLIS-COMPOS\\Desktop\\colors\\Potrace Tester')
os.chdir('C:\\Users\\burak\\Google Drive\\Python Files\\PNG2Acrylic')

def sphericalsurface_nthlayer(n):
#creates an voxel surface using a radius of n, where n is an integer
#creates a list of increment values in x,y,z that should be used to increment a pixel's coordinate to obtain the surface.
#returns a list of increment values in (x,y,z) - all values are integers

    def dist(index):
        return math.sqrt(index[0]*index[0]+index[1]*index[1]+index[2]*index[2])
    
    if n==0:
        templist=[(0,0,0)]
    elif n>0:
        for d in range(n-1,n+1):
            mn=2*d+1
            templist=[]
            for k in range(mn):
                for j in range(mn):
                    for i in range(mn):
                        tempindex=(-d+i,-d+j,-d+k)
                        if dist(tempindex)<=d and dist(tempindex)>(d-1):
                            templist.append(tempindex)
    return templist

palettedef=((0,0,0),(204,0,166),(236,175,237),(123,125,146),(33,33,34),(197,161,127),(186,176,85),(178,210,80),(245,242,199),(119,196,245),(166,233,248),(233,17,140),(250,218,157),(253,176,159),(223,183,60),(255,255,255))
#this is the palette for the Art Marker Alcohol Ink on Glossy Photo Paper

#copy the palettedef to a new list called templist
#templist=[]
#for color in palettedef:
#    templist.append(color)

#colormapdict={}
# colormapdict stores the final color space that maps every color in (R,G,B) to one of the colors on the palette.

#CREATE A NEW SUBROUTINE CALLED "mapcolorspace2palette(palettedef)" where palettedef is a tuple containint a bunch of (r,g,b) codes that are obtained from the color palette to be used.
def mapcolorspace2palette(palette):
    #copy the palettedef to a new list called templist
    templist=[]
    for color in palette:
        templist.append(color)
    colormapdict={}

    ct=0
    while ct <= 444:
        t0=time.time()
        incrementlist=sphericalsurface_nthlayer(ct) #creates a list of voxels (r,g,b) that form a shperical surface of radius ct voxels
        tf=time.time()
        print ('ct is  ', ct, 'time for spherical surface gen is ', tf-t0)        
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
        print ('it took ', time.time()-tf,' to map the spherical surface for each color on the list')
        if len(templist)<1:
            maxcount=ct
            ct=500
            print ('max diameter of expanding spheres was  ', maxcount, ' pixels')
        ct=ct+1
    return colormapdict

t00=time.time()
newcolormapdict=mapcolorspace2palette(palettedef)
print('**********')
print('mapping the whole palette took ', time.time()-t00)

def writecolormapdictionary2file(colormapdict,filename):
#following code saves the dictionary colormapdict to a text file (result is around 500MB)
    with open(filename,"w") as outputfile:
        for keys in colormapdict:
            tempstr=str(keys)+':'+str(colormapdict[keys])+'\n'
            x=outputfile.write(tempstr)

a0=writecolormapdictionary2file(newcolormapdict,'ArtMarkerPaletteColorMapDict.txt')