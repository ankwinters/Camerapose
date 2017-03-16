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
import re
import os
from quaternion import Quaternion


def CamCirclePos(center,r,k=360):
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
        y = center[1]
        z = math.sqrt(r*r-x*x)
        #print((x,y,z))
        cam.append((round(x,preci),round(y,preci),round(z,preci)))
    for item in reversed(cam):
        cam.append((item[0],item[1],-item[2]))
    return cam

def CamSpherePos(center,r,k):
    pass

def DeterminUpRight(loc,look_at,ratio=(4,3)):
# Cam-look_at vector to rotation matrix & translation vector
    vec = np.array(loc)-np.array(look_at)
# Right vector,make vec.dot(rig)=0
    rig_vec = np.array((-vec[(2)],0,vec[(0)]))
# normalize
    right = rig_vec/np.sqrt(rig_vec.dot(rig_vec))
    #print("vec dot right:",vec," * ", right, vec.dot(right))
    up_vec = -np.cross(vec,right)
    up = up_vec/np.sqrt(up_vec.dot(up_vec))

# default film size: 4mm*3mm
    return tuple(up*int(ratio[1])/1000),tuple(right*int(ratio[0])/1000)

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
# Step1: Rotate z to _z, vec(0,0,1)->vec(cam_z)
    theta_z = arccos( np.dot(cam_z,np.array((0,0,1))) )
    # if theta_z =180.0 or 0,then the axis would be either x or y
    rot_axis_z = np.array((1,0,0))
    if theta_z < 180.0 and theta_z > 0.01:
        rot_axis_z = np.cross(np.array((0,0,1)),cam_z)
    qz = Quaternion.from_axisangle(theta_z,rot_axis_z)
    print("theta_z",theta_z," rot_axis_z",rot_axis_z," qz",qz)
# Step2: Rotate x to _x,vec(1,0,0)-> Rz*vec(cam_x)
    cam_x_qz = qz*cam_x
    theta_x = arccos( np.dot(cam_x_qz, np.array((1,0,0))) )
    # if theta_x =180.0,then the axis would be y or z
    rot_axis_x = np.array((0,1,0))
    if theta_x < 180.0 and theta_x > 0.01:
        rot_axis_x = np.cross(np.array((1,0,0)), cam_x_qz) 
    qx = Quaternion.from_axisangle(theta_x,rot_axis_x)
    print("theta_x",theta_x," rot_axis_x",rot_axis_x," qx",qx)
# Step3: Combine qz & qx
    q = qz*qx
    #print(q)
    #print(Quaternion.get_rotation_matrix(q))
    rotate = Quaternion.get_rotation_matrix(q)
    trans = _z
# Output put R t
    rt = np.column_stack((rotate,trans))
    return np.reshape(rt,12)
    
    #return np.hstack((rotate,trans.transpose()))

def GenPovFile(template_file, cam_loc, look_at, up, right, out_file_dir, out_file_name):
#TODO: Change "direction" line
    output_file = out_file_dir+"/"+out_file_name

    def write_to_string(loc):
        return "<"+str(loc[0])+", "+str(loc[1])+", "+str(loc[2])+">"

    cam_string = write_to_string(cam_loc)
    look_string = write_to_string(look_at)
    up_string = write_to_string(up)
    right_string = write_to_string(right)

    with open(template_file, "r") as sources:
        lines = sources.readlines()
    with open(output_file, "w") as sources:
        for line in lines:
            write_line = re.sub(r'^(\s+location\s+)(<.*?>)', r'\1'+cam_string, line)  
            write_line = re.sub(r'^(\s+up\s+)(<.*?>)', r'\1'+up_string, write_line)  
            write_line = re.sub(r'^(\s+right\s+)(<.*?>)',r'\1'+right_string, write_line)
            write_line = re.sub(r'^(\s+look_at\s+)(<.*?>)',r'\1'+look_string, write_line)
            sources.write(write_line)
    print("Generating file ",output_file)
    
def PovToImg(pov_path, img_path):
    print("Creating image: ",img_path)
    os.system("povray -W1024 -H768 +I"+pov_path+" +O"+img_path+" >/dev/null 2>&1")


def save_rt_paras(rt_list, out_path):
    with open(out_path, 'w') as fp: 
        for rt in rt_list:
            np.savetxt(fp, rt_list, "%.6f "*12)


def GenOutFiles(template_file,dst_dir):
    ''' 
    Input: /path/to/template.pov, output_directory(e.g.: /tmp/dataset)
    parameters: generate 360 files where 
    camera is located where is 3m in front of object
    '''
    file_counts = 180
    distance = 3
    look_at = (0, 0.7, 0)
    pov_out_dir = dst_dir+"/pov_files"
    img_out_dir = dst_dir+"/img_files"
    pose_file = dst_dir+"/Camerapose.txt"

    cameras = CamCirclePos(look_at, distance, file_counts)
    count = 0
    for cam in cameras:
        up,right = DeterminUpRight(cam, look_at)
        pov_out_name = '{:06d}'.format(count)+'.pov'
        img_out_name = '{:06d}'.format(count)+'.png'
        GenPovFile(template_file, cam, look_at, up, right, pov_out_dir, pov_out_name)
        #PovToImg(pov_out_dir+"/"+pov_out_name, img_out_dir+"/"+img_out_name)
        count+=1
    
     

if __name__=="__main__":
    #cam = CamCircle((0,0,0),2,6)
    #DeterminRight(cam[0],(0,0,0))
    pose = SinglePoseTrans((0,0,1),(0,0,0),(0.707,0.707,0))
    new = []
    for i in range(0,1):

        new.append(pose)

    save_rt_paras(new,"/tmp/list.txt")
    #GenPovFile( "/tmp/gt.pov", (0,1,1), (3,4,5), (7,8,9), (9,10,11),"/tmp","1.pov")
    #PovToImg("/tmp/1.pov","/tmp/1.png")
    #GenOutFiles("./gt.pov","./mono3m")
