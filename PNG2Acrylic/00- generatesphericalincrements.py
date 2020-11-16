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

def generatesphericalsurfaces_on_file():
#creates a text file where each line in file corresponds to a list of increment values in x,y,z that should be used to increment a pixel's coordinate to obtain the surface.
#all values are integers
    outputfile=open('sphericalsurfaces.txt',"w")
    maxradius=255
    t00=time.time()
    for i in range(0,maxradius):
        t0=time.time()
        templist=tuple(sphericalsurface_nthlayer(i))
        tempstr=str(templist)+'\n'
        x=outputfile.write(tempstr)
        print('r= ', i, 'time to calculate and write to file: ',time.time()-t0)
    outputfile.close()
    print('ran maxradius of: ',maxradius, 'in ', time.time()-t00, 'seconds')

#generatesphericalsurfaces_on_file()

def generatesphericalsurfaces_on_binaryfile():
#creates a text file where each line in file corresponds to a list of increment values in x,y,z that should be used to increment a pixel's coordinate to obtain the surface.
#all values are integers
    outputfile=open('sphericalsurfaces_bin.txt',"wb")
    maxradius=255
    t00=time.time()
    for i in range(0,maxradius):
        t0=time.time()
        templist=tuple(sphericalsurface_nthlayer(i))
        tempstr=str(templist)+'\n'
        bpop=tempstr.encode('utf-8')
        x=outputfile.write(bpop)
        print('r= ', i, 'time to calculate and write to file: ',time.time()-t0)
    outputfile.close()
    print('ran maxradius of: ',maxradius, 'in ', time.time()-t00, 'seconds')

generatesphericalsurfaces_on_binaryfile()

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

spherical_surfaceincrements_list=readsphericalsurfaceincrements()