#!/usr/bin/env python3
"""
利用给定的目标中心(x,y,z)，以及半径r，生成一定数量相机位置k，并输出对应的R|t
Input:(x,y,z),r,k
Output:1.pov,2.pov,3.pov,...,k.pov
       Camarapose.txt 
By default: left-handed

"""
import random
import math
import numpy as np
def CamCircleLocation(center,r,k):
# This function is an easy pose generator.The output forms as a circle in the plane y=y_center.
# x^2+z^2=r^2
# Output: cam[(x1,y,z1),(x2,y,z2),...,(xk,y,zk)]
    preci=8
    random.seed()
    cam=[]
    if k % 2 != 0:
        print("Error input k:", k)
        exit(-1)
# Determine the average gap between two sequence x-coordinates
    gap = 2*r/(k+1)
    for i in range(1,k+1):
        #x = -r+gap*(i-1)+gap*random.random()
        x = -r+gap*(i-1)+gap*1
        y = 0
        z = math.sqrt(r*r-x*x)
        #print((x,y,z))
        cam.append((round(x,preci),round(y,preci),round(z,preci)))
    for item in reversed(cam):
        cam.append((item[0],item[1],-item[2]))
    return cam

def DeterminRight(loc,look_at):
# Cam-look_at vector to rotation matrix & translation vector
    vec = np.array(loc)-np.array(look_at)
# Right vector,make vec.dot(rig)=0
    rig = np.array((-vec[(2)],0,vec[(0)]))
# normalize
    right = rig/np.sqrt(rig.dot(rig))
    print("vec dot right:",vec," * ", right, vec.dot(right))
    return tuple(right)

def SinglePoseTrans(

if __name__=="__main__":
    cam = CamCircleLocation((0,0,0),2,6)
    DeterminRight(cam[0],(0,0,0))
