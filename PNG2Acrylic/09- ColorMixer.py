import os;import time;import json;import math;import re;import random
os.chdir('C:\\Users\\buzman.CORIOLIS-COMPOS\\Desktop\\Python Files\\Python Files\\PNG2Acrylic')

import PIL
from PIL import Image
import re
from ast import literal_eval


def RGB2HSV(tup0):
    (R,G,B)=tup0 #tup0 is a tuple of standard RGB values (R,G,B) in range 0 to 255
    #algorithm returns a tuple (H,S,V) where H is in range 0 to 360, S and V are in range 0 to 255
    #R, G and B (Standard RGB) input range=0 to 255

    red=R/255
    green =G/255
    blue =B/255

    color_min=min(red, green, blue)   
    color_max=max(red, green, blue)  
    chroma=color_max-color_min

    V=color_max

    if chroma==0 :
        H=0
        S=0
    else:
        S=chroma/color_max
        del_R =(((color_max-red )/6 )+(chroma/2))/chroma
        del_G =(((color_max-green )/6 )+(chroma/2))/chroma
        del_B =(((color_max-blue )/6 )+(chroma/2))/chroma
        if red==color_max:
            H=del_B-del_G #H, S and V output range=0 to 1.0
        elif green==color_max:
            H =(1/3 )+del_R-del_B  #H, S and V output range=0 to 1.0
        elif blue==color_max:
            H =(2/3 )+del_G-del_R  #H, S and V output range=0 to 1.0

        if H<0:
            H=H+1
        if H>1:
            H=H-1

    H=int(H*360) #Scale Hue to range 0 to 360
    #S=S*255 #Scale Saturation to range 0 to 255
    #V=V*255 #Scale Value to range 0 to 255
        
    return (H,S,V)

def HSV2RGB(tup0):
    (H,S,V)=tup0
    #R, G and B (Standard RGB) input range=0 to 255
    #Normalize H, S and V to range 0 to 1.0
    H=H/360
    #S=S/255
    #V=V/255

    if S == 0:
       red = V
       green = V
       blue = V
    else:
        var_h = H * 6

        if var_h == 6:
            var_h = 0      #H must be < 1

        var_i = int( var_h )
        var_1 = V * ( 1 - S )
        var_2 = V * ( 1 - S * ( var_h - var_i ) )
        var_3 = V * ( 1 - S * ( 1 - ( var_h - var_i ) ) )

        if var_i == 0:
            red = V
            green = var_3
            blue = var_1
        elif var_i == 1:
            red = var_2
            green = V
            blue = var_1
        elif var_i == 2 :
            red = var_1
            green = V
            blue = var_3
        elif var_i == 3:
            red = var_1
            green = var_2
            blue = V
        elif var_i == 4:
            red = var_3
            green = var_1
            blue = V
        else:
            red = V
            green = var_1
            blue = var_2

    R = int(red * 255)
    G = int(green * 255)
    B = int(blue * 255)
    
    return (R,G,B)
	
def RGB2XYZ(tup0):
    (R,G,B)=tup0
    #R, G and B (Standard RGB) input range=0 to 255

    red=R/255 #normalize red
    green=G/255 #normalize green
    blue=B/255 #normalize blue

    if red>0.04045:
        red_linear=math.pow(((red+0.055)/1.055),2.4)
    else:
        red_linear=red/12.92
    if green>0.04045:
        green_linear=math.pow(((green+0.055)/1.055),2.4)
    else:
        green_linear=green/12.92
    if blue>0.04045:
        blue_linear=math.pow(((blue+0.055)/1.055),2.4)
    else:
        blue_linear=blue/12.92
	#these red, blue, and green are linearized r,g,b. They are gamma adjusted, where gamma is 2.4 per sRGB
	
    red_linear=red_linear*100
    green_linear=green_linear*100
    blue_linear=blue_linear*100

    X=red_linear*0.4124+green_linear*0.3576+blue_linear*0.1805
    Y=red_linear*0.2126+green_linear*0.7152+blue_linear*0.0722
    Z=red_linear*0.0193+green_linear*0.1192+blue_linear*0.9505
    
    #Reference-X, Y and Z refer to specific illuminants and observers.
    #Use D65 Reference X, Y,Z values for 2 degrees (CIE 1931) for sRGB
    #Reference_X=95.047 #D65 Reference X, Y,Z values for 2 degrees (CIE 1931)
    #Reference_Y=100.000 #D65 Reference X, Y,Z values for 2 degrees (CIE 1931)
    #Reference_Z=108.883 #D65 Reference X, Y,Z values for 2 degrees (CIE 1931)
    Reference_X=100
    Reference_Y=100
    Reference_Z=100
    
    
    X=X/Reference_X
    Y=Y/Reference_Y
    Z=Z/Reference_Z
    
    return (X,Y,Z)

def XYZ2RGB(tup0):

    (X,Y,Z)=tup0
     
    red_linear=X*3.2404542+(-1.5371385)*Y+(-0.4985314)*Z
    green_linear=X*(-0.9692660)+Y*1.8760108+Z*0.0415560
    blue_linear=X*0.0556434+Y*(-0.2040259)+Z*1.0572252

    if red_linear<=0: red_linear=0
    if green_linear<=0:green_linear=0
    if blue_linear<=0: blue_linear=0
    
    if(red_linear>0.0031308):
        red=1.055 * math.pow(red_linear,0.4166666)-0.055
    elif red_linear>=0:
        red=12.92*red_linear
    else:
        red=0
        
    if(green_linear>0.0031308):
        green=1.055* math.pow(green_linear,0.4166666)-0.055
    elif green_linear>=0:
        green=12.92*green_linear
    else:
        green=0
        
    if(blue_linear>0.0031308):
        blue=1.055* math.pow(blue_linear,0.4166666)-0.055
    elif blue_linear>=0:
        blue=12.92*blue_linear
    else:
        blue=0
    
    if red>=1: red=1
    if green>=1: green=1
    if blue>=1: blue=1

    R=int(red*255)
    G=int(green*255)
    B=int(blue*255)
    
    return (R,G,B)
    
def RGB2Lab(tup0):
    (R,G,B)=tup0
    #R, G and B (Standard RGB) input range=0 to 255

    red=R/255 #normalize red
    green=G/255 #normalize green
    blue=B/255 #normalize blue

    if red>0.04045:
        red=math.pow(((red+0.055)/1.055),2.4)
    else:
        red=red/12.92
    if green>0.04045:
        green=math.pow(((green+0.055)/1.055),2.4)
    else:
        green=green/12.92
    if blue>0.04045:
        blue=math.pow(((blue+0.055)/1.055),2.4)
    else:
        blue=blue/12.92

    red=red*100
    green=green*100
    blue=blue*100

    X=red*0.4124+green*0.3576+blue*0.1805
    Y=red*0.2126+green*0.7152+blue*0.0722
    Z=red*0.0193+green*0.1192+blue*0.9505
    
    #Reference-X, Y and Z refer to specific illuminants and observers.
    #Use D65 Reference X, Y,Z values for 2 degrees (CIE 1931) for sRGB
    Reference_X=95.047 #D65 Reference X, Y,Z values for 2 degrees (CIE 1931)
    Reference_Y=100.000 #D65 Reference X, Y,Z values for 2 degrees (CIE 1931)
    Reference_Z=108.883 #D65 Reference X, Y,Z values for 2 degrees (CIE 1931)
	
    X=X/Reference_X
    Y=Y/Reference_Y
    Z=Z/Reference_Z

    if X>0.008856:
        X=math.pow(X,(1/3))
    else:
        X=(7.787*X)+(16/116)
    if Y>0.008856:
        Y=math.pow(Y,(1/3))
    else:
        Y=(7.787*Y)+(16/116)
    if Z>0.008856: 
        Z=math.pow(Z,(1/3))
    else:
        Z=(7.787*Z)+(16/116)

    CIE_L=(116*Y)-16
    CIE_a=500*(X-Y)
    CIE_b=200*(Y-Z)
    
    return (CIE_L,CIE_a,CIE_b)
    
def Lab2RGB(tup0):

    (CIE_L,CIE_a,CIE_b)=tup0
    fy=(CIE_L+16)/116
    fx=CIE_a/500+fy
    fz=fy-CIE_b/200
    
    epsilon=0.008856
    kappa= 903.3
    
    if fx*fx*fx>epsilon:
        xr=fx*fx*fx
    else:
        xr=(116*fx-16)/kappa
    
    if CIE_L>epsilon*kappa:
        yrp=(CIE_L+16)/116
        yr=yrp*yrp*yrp
    else:
        yr=CIE_L/kappa
        
    if fz*fz*fz>epsilon:
        zr=fz*fz*fz
    else:
        zr=(116*fz-16)/kappa
    
    #Reference_X, Y and Z refer to specific illuminants and observers.
    #Use D65 Reference X, Y,Z values for 2 degrees (CIE 1931) for sRGB
    #(X_r, Y_r, Z_r) is the reference white
    # D65= (0.95047,1.00000,1.08883)
    # D55= (0.95682,1.00000,0.92149)
    # D50= (0.96422,1.00000,0.82521)
    (X_r, Y_r, Z_r) = (0.95047,1.00000,1.08883)
    
    X=xr*X_r
    Y=yr*Y_r
    Z=zr*Z_r
    

    red_linear=X*3.2404542+(-1.5371385)*Y+(-0.4985314)*Z
    green_linear=X*(-0.9692660)+Y*1.8760108+Z*0.0415560
    blue_linear=X*0.0556434+Y*(-0.2040259)+Z*1.0572252

    if red_linear<=0: red=0
    if green_linear<=0:green=0
    if blue_linear<=0: blue=0
    
    if(red_linear>0.0031308):
        red=1.055 * math.pow(red_linear,0.4166666)-0.055
    elif red_linear>=0:
        red=12.92*red_linear
    else:
        red=0
        
    if(green_linear>0.0031308):
        green=1.055* math.pow(green_linear,0.4166666)-0.055
    elif green_linear>=0:
        green=12.92*green_linear
    else:
        green=0
        
    if(blue_linear>0.0031308):
        blue=1.055* math.pow(blue_linear,0.4166666)-0.055
    elif blue_linear>=0:
        blue=12.92*blue_linear
    else:
        blue=0
    
    if red>=1: red=1
    if green>=1: green=1
    if blue>=1: blue=1

    R=int(red*255)
    G=int(green*255)
    B=int(blue*255)
    
    return (R,G,B)

def colormix_xyz(color1,color2,r1,r2):
#To mix colors one has to use linear color space like XYZ or linearized rgb (adjusted for gamma of the sRGB color space).
#This function uses the linear XYZ interpolation

    image_height=1000 #pixels
    image_width=1000 #pixels
    perc1=r1/(r1+r2)
    perc2=1-perc1
    outputimage=Image.new('RGB',(2*image_width,image_height))
    outputimage_pixelmap=outputimage.load()
    col1=RGB2XYZ(color1)
    col2=RGB2XYZ(color2)
    xyz_linear=((col1[0]*perc1+col2[0]*perc2),(col1[1]*perc1+col2[1]*perc2),(col1[2]*perc1+col2[2]*perc2))
    rgb_linearmix=XYZ2RGB(xyz_linear)
    #Next 2 nested for loops output 2 images side by side. First image is linear optical mix of color1 and color2. Second image is the resultant rgb_linearmix
    for j in range(image_height): #randomize the distribution of color1 and color2 proportional to r1 and r2
        for i in range(image_width):
            rn=random.random() 
            if rn<=perc1:
                pixcolor=color1
            else:
                pixcolor=color2
            outputimage_pixelmap[i,j]=pixcolor
    for j in range(image_height): 
        for i in range(image_width+1,2*image_width):
            outputimage_pixelmap[i,j]=rgb_linearmix
    outputimage.save('temp-xyzavg.png')
    outputimage.show()