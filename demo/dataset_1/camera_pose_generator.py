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

from time import sleep


def hand_trans(_loc):
    # TODO: We make it be the intermediate
    return np.array((_loc[0], _loc[1], -_loc[2]))


def CamCirclePos(center, r, count=360, preci=8):
    # This function is an easy pose generator.The output forms as a circle in the plane y=y_center.
    # x^2+z^2=r^2
    # Output: cam[(x1,y,z1),(x2,y,z2),...,(xk,y,zk)]
    # use parameterized (x,y,z) in right-handed system
    # change order
    # z = r*cos\theta
    # x = r*sin\theta
    # y = y0
    # 0<theta<2*pi
    random.seed()
    cam = []
# Initial cam
    cam.append(
        hand_trans((round(0, preci), round(center[1], preci), round(r, preci))))
    if count < 1:
        print("Num of count error.count should be at least 1")
        return cam
    elif count == 1:
        return cam
    else:
        cnt = count - 1
# Fill remaining cams
    gap = 2 * math.pi / count
    for i in range(0, cnt):
        #theta = random.random()*(i+1)/cnt*(2*math.pi)
        theta = i * gap + (random.random() * 0.5 + 0.5) * gap
        z = r * math.cos(theta)
        y = center[1]
        x = r * math.sin(theta)
        cam.append(
            hand_trans((round(x, preci), round(y, preci), round(z, preci))))

    return cam


def CamRandomPos(center, r, count=1, preci=8):
    # use parameterized (x,y,z) in right-handed system
    # change order
    # z = x0+r*cos\theta*sin\phi
    # x = y0+r*sin\theta*sin\phi
    # y = z0+r*cos\phi
    # 0<theta<2*pi,0<phi<pi
    cam = []
    random.seed()
    for i in range(0, count):
        theta = random.random() * math.pi * 2
# TODO: You need to make a better model.At present,phi is between pi/6 & 5*pi/6
        #phi = random.random()*math.pi
# [pi/6,pi/2)
        phi = (random.random() * 1 / 3 + 1 / 6) * math.pi
        z = center[0] + r * math.cos(theta) * math.sin(phi)
        x = center[1] + r * math.sin(theta) * math.sin(phi)
        y = center[2] + r * math.cos(phi)
        cam.append(
            hand_trans((round(x, preci), round(y, preci), round(z, preci))))
    return cam


def DeterminUpRight(loc, look_at, ratio=(4, 3)):
    # It's based on left-handed coordinate system.
    # So it's need to be transformed after calculation in right-handed coordinates
    # Cam-look_at vector to rotation matrix & translation vector
    vec = hand_trans(np.array(loc) - np.array(look_at))
# Right vector,make vec.dot(rig)=0
    #rig_vec = np.array((-vec[(2)],0,vec[(0)]))
    world_up = np.array((0, 1, 0))
    if np.linalg.norm(vec) == 0:
        print("error")
        exit(-1)
    rig_vec = np.cross(world_up, vec)
# normalize
    right = rig_vec / np.sqrt(rig_vec.dot(rig_vec))
    up_vec = np.cross(vec, right)
    up = up_vec / np.sqrt(up_vec.dot(up_vec))
# default film size: 4mm*3mm
    #print("In right-handed system, vec:",vec," right:", right, " up:",up)
    return hand_trans(up) * int(ratio[1]) / 1000,\
        hand_trans(right) * int(ratio[0]) / 1000


def DeterminDirect(cam, look_at):
    pass


def SinglePoseTrans(loc, look_at, right):
    # It's based on right-handed coordinate system.
    # z-axis:vec = loc-look_at,
    # x-axis:right,vector
    # Now it's time for y-axis
    # fix:loc & look_at could be np.array
    if tuple(loc) == tuple(look_at):
        return "error"
# t_vec+vec_=vec_in_world, _z=t_vec
    #_z = np.array(loc)-np.array(look_at)
    _rig_loc = hand_trans(np.array(loc))
    _rig_lookat = hand_trans(np.array(look_at))
# Camera reverse
    _z = _rig_lookat - _rig_loc
    _x = hand_trans(np.array(right))
# Normalize
    cam_z = _z / np.sqrt(_z.dot(_z))
    cam_x = _x / np.sqrt(_x.dot(_x))
    #print("In right-handed system, cam_z:",cam_z," cam_x:", cam_x)
# Right-handed
    print("cam_z:", _rig_loc, "->(0,0,0)")
# Use quaterunion method

    def arccos(cos_theta):
        if cos_theta > 0.9999:
            cos_theta = 1.0
        elif cos_theta < -0.9999:
            cos_theta = -1.0
        return math.degrees(math.acos(cos_theta))
# Step1: Rotate from z to _z, that is vec(cam_z)(in world) -> (0,0,1)(in cam)
    theta_z = arccos(np.dot(cam_z, np.array((0, 0, 1))))
    # if theta_z =180.0 or 0,then the axis would be either x or y
    rot_axis_z = np.array((1, 0, 0))
    if theta_z < 179.99 and theta_z > 0.01:
        rot_axis_z = np.cross(cam_z, np.array((0, 0, 1)))
        #rot_axis_z = np.cross(np.array((0,0,1)),cam_z)
    # world_coordnate ->(0,0,1)(camera coordinate)
    qz = Quaternion.from_axisangle(theta_z, rot_axis_z)
# Step2: Rotate x to _x,that is vec(cam_z)(in world) -> (1,0,0)(in cam)
    world_x_qz = qz * cam_x
    #world_x_qz = qz*np.array((1,0,0))
    # print("world_x_qz:",world_x_qz)
    #theta_x = arccos( np.dot(cam_x, world_x_qz) )
    theta_x = arccos(np.dot(np.array((1, 0, 0)), world_x_qz))
    # if theta_x =180.0,then the axis would be y or z
    rot_axis_x = np.array((0, 0, 1))
    #rot_axis_x = np.array((1,0,0))
    if theta_x < 179.99 and theta_x > 0.01:
        #rot_axis_x = np.cross(world_x_qz,cam_x)
        rot_axis_x = np.cross(np.array((1, 0, 0)), world_x_qz)
# Step3: Combine qz & qx,reverse
    qz = Quaternion.from_axisangle(theta_z, -rot_axis_z)
    print("theta_z:", theta_z, " rot_axis_z:", -rot_axis_z, " qz", qz)
    qx = Quaternion.from_axisangle(theta_x, -rot_axis_x)
    print("theta_x", theta_x, " rot_axis_x", -rot_axis_x, " qx", qx)
    q = qz * qx
    # print(q)
    # print(Quaternion.get_rotation_matrix(q))
# Get rotation matrix
    rotate = Quaternion.get_rotation_matrix(q)
# bug fix2 : trans should not be confused with _z vector
    trans = _rig_loc
# Output put R t
    rt = np.column_stack((rotate, trans))
    return np.reshape(rt, (1, 12))


def GenPovFile(template_file, cam_loc, direction, look_at,
               up, right, out_file_dir, out_file_name):
    # TODO: Change "direction" line
    output_file = out_file_dir + "/" + out_file_name

    def write_to_string(loc):
        return "<" + str(loc[0]) + ", " + str(loc[1]) + \
            ", " + str(loc[2]) + ">"

    cam_string = write_to_string(cam_loc)
    direc_string = write_to_string(direction)
    look_string = write_to_string(look_at)
    up_string = write_to_string(up)
    right_string = write_to_string(right)

    with open(template_file, "r") as sources:
        lines = sources.readlines()
    with open(output_file, "w") as sources:
        for line in lines:
            write_line = re.sub(
                r'^(\s+location\s+)(<.*?>)',
                r'\1' + cam_string,
                line)
        # TODO: it's a hacked version only for circle cams
            write_line = re.sub(
                r'^(\s+direction\s+)(<.*?>)',
                r'\1' + direc_string,
                write_line)
            write_line = re.sub(
                r'^(\s+up\s+)(<.*?>)',
                r'\1' + up_string,
                write_line)
            write_line = re.sub(
                r'^(\s+right\s+)(<.*?>)',
                r'\1' + right_string,
                write_line)
            write_line = re.sub(
                r'^(\s+look_at\s+)(<.*?>)',
                r'\1' + look_string,
                write_line)
            sources.write(write_line)
    print("Generating file ", output_file)


def PovToImg(pov_path, img_path, wid=2560, hei=1920):
    print("Creating image: ", img_path)
    if wid / hei == 4 / 3:
        size = "-W" + str(wid) + " -H" + str(hei)
    else:
        print("Warning:size fallback to default:2560*1920")
        size = "-W2560 -H1920"
    os.system("povray " + size +
              " -D +I" + pov_path +
              " +O" + img_path +
              " >/dev/null 2>&1")


def save_rt_paras(rt_list, out_path):
    with open(out_path, 'wb') as fp:
        for rt in rt_list:
            np.savetxt(fp, rt, "%f," * 4 + ";" + "%f," * 4 + ";" + "%f," * 4)


def GenCams(template_file, dst_dir, pose_file, pov_dir_name,
            img_dir_name, flag=0, file_counts=360, distance=3,
            look_at=(0, 0.7, 0), focal_len=0.005):
    '''
    Input: /path/to/template.pov, output_directory(e.g.: /tmp/dataset)
    if flag==0, that means run in circle mode.
    Besides, run in random mode
    *circle mode:
    generate images where
    camera is arranged uniformly in a circle with specific paras.
    *random mode:
    generate images where
    camera is arranged randomly in a sphere with specific paras.
    '''
    #file_counts = 4
    #distance = 3
    #look_at = (0, 0.7, 0)
    direc_pos = (0, 0, focal_len)
# bug fix: direc neg should be negative
    direc_neg = (0, 0, -focal_len)
    pov_out_dir = dst_dir + "/" + pov_dir_name
    img_out_dir = dst_dir + "/" + img_dir_name
    pose_file = dst_dir + "/" + pose_file
    if flag == 0:
        cameras = CamCirclePos(look_at, distance, file_counts)
    else:
        cameras = CamRandomPos(look_at, distance, file_counts)
    count = 0
    rt_list = []
    cur_dir = os.getcwd()
    for cam in cameras:
        up, right = DeterminUpRight(cam, look_at)
        #print("cam:",cam," up:",up," right:",right)
        pov_out_name = '{:06d}'.format(count) + '.pov'
        img_out_name = '{:06d}'.format(count) + '.png'
# TODO: a hack version
        if cam[2] < 0:
            direction = direc_pos
        else:
            direction = direc_neg
        GenPovFile(
            template_file,
            cam,
            direction,
            look_at,
            up,
            right,
            pov_out_dir,
            pov_out_name)
        rt = SinglePoseTrans(cam, look_at, right)
        rt_list.append(rt)
        PovToImg(
            pov_out_dir +
            "/" +
            pov_out_name,
            img_out_dir +
            "/" +
            img_out_name)
        count += 1
    save_rt_paras(rt_list, pose_file)


def test():
    cams = CamRandomPos((0, 0.7, 0), 3, 10)
    print(cams)


if __name__ == "__main__":
    #cam = CamCircle((0,0,0),2,6)
    # DeterminRight(cam[0],(0,0,0))
    pose = SinglePoseTrans((1, 0, 0), (0, 0, 0), (0, 0, 0.707))
    print(pose)
    #new = []
    # test()

    # save_rt_paras(new,"/tmp/list.txt")
    #GenPovFile( "/tmp/gt.pov", (0,1,1), (3,4,5), (7,8,9), (9,10,11),"/tmp","1.pov")
    # PovToImg("/tmp/1.pov","/tmp/1.png")
    # for i in range(11,20):
    #    focal = 5*(i+1)//2-10
    #    ClearFiles("./mono3m")
    #    GenCircleCams("./gt.pov","./mono3m",file_counts=5,distance=i,look_at=(0, 0.7, 0),focal_len=focal/1000)
    #    os.system("cp -r ./mono3m ../../mve_result/gt_%2dm" % i)
