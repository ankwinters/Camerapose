#!/usr/bin/env python3
"""
利用给定的目标中心(x,y,z)，以及半径r，生成一定数量相机位置k，并输出对应的R|t
Input:(x,y,z),r,k
Output:1.pov,2.pov,3.pov,...,k.pov
       Camarapose.txt 
By default: right-handed

"""
import random
import math
import numpy as np
from quaternion import Quaternion


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

def SinglePoseTrans(loc, look_at, right):
# z-axis:vec = loc-look_at,
# x-axis:right,vector
# Now it's time for y-axis  
    if loc==look_at:
        return "error"
    _z = np.array(loc)-np.array(look_at)
    _x = np.array(right)
# Normalize
    cam_z = _z/np.sqrt(_z.dot(_z))
    cam_x = _x/np.sqrt(_x.dot(_x))
# Right-handed
# Use quaterunion method
    def arccos(cos_theta):
        return math.degrees(math.acos(cos_theta))
# Step1: Rotate _z to z, vec(cam_z)->vec(0,0,1)
    theta_z = arccos( np.dot(cam_z,np.array((0,0,1))) )
    if theta_z < 180.0:
        rot_axis_z = np.cross(cam_z,np.array((0,0,1)))
    else:
        rot_axis_z = np.array((0,0,1))
    qz = Quaternion.from_axisangle(theta_z,rot_axis_z)
    print("theta_z",theta_z," rot_axis_z",rot_axis_z," qz",qz)
# Step2: Rotate _x to z, Rz*vec(cam_x)->vec(1,0,0)
    #cam_x_qz = qz*cam_x
    cam_x_qz = cam_x
    theta_x = arccos( np.dot(cam_x_qz, np.array((1,0,0))) )
    if theta_x < 180.0:
        rot_axis_x = np.cross(cam_x_qz,np.array((1,0,0))) 
    else:
        rot_axis_x = np.array((1,0,0))
    qx = Quaternion.from_axisangle(theta_x,rot_axis_x)
    print("theta_x",theta_x," rot_axis_x",rot_axis_x," qx",qx)
# Step3: Combine qz & qx
    q = qz*qx
    print(q)


     

if __name__=="__main__":
    #cam = CamCircleLocation((0,0,0),2,6)
    #DeterminRight(cam[0],(0,0,0))
    SinglePoseTrans((0,0,-1),(0,0,0),(0.707,0.707,0))
