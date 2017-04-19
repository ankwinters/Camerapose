#!/usr/bin/env python3

import camera_pose_generator as pg

import os
import fnmatch
import shutil


class Stereo:

    def __init__(self, template, obj_dir, baseline=0.10, file_counts=360,
                 distance=3, look_at=(0, 0.7, 0), focal_len=0.005, ratio=(4, 3)):
        self.template = template
        self.objdir = obj_dir

        self.baseline = baseline
        self.cnts = file_counts
        self.dist = distance
        self.focal = focal_len
        self.look = look_at
        self.ratio = ratio

        # set output dir
        self.povdir = self.objdir + "/pov"
        self.imgdir = self.objdir + "/img"
        self.povleft = self.povdir + "/left"
        self.povright = self.povdir + "/right"
        self.imgleft = self.imgdir + "/left"
        self.imgright = self.imgdir + "/right"

        if os.path.isdir(self.objdir):
            # remove all files under the existing dir
            if os.path.isdir(self.povdir):
                shutil.rmtree(self.povdir)
            if os.path.isdir(self.imgdir):
                shutil.rmtree(self.imgdir)
        else:
            os.mkdir(self.objdir)

        os.makedirs(self.povleft)
        os.makedirs(self.povright)
        os.makedirs(self.imgleft)
        os.makedirs(self.imgright)

    # The stereo cameras are assumed to be rectified.
    def right_cam_gen(self, left_cam, rig_vec):
        rig_cam = []
        for cam, rig in zip(left_cam, rig_vec):
            # print(rig)
            rig_loc = cam + rig / int(self.ratio[0]) * 1000 * self.baseline
            rig_cam.append(rig_loc)
        return rig_cam

    def UpRight_vec_gen(self, left_cam):
        Up = []
        Right = []
        for cam in left_cam:
            up, rig = pg.DeterminUpRight(cam, self.look, self.ratio)
            Up.append(up)
            Right.append(rig)
        return Up, Right

    def cam_circle_pose(self):
        left_cam = pg.CamCirclePos(self.look, self.dist, self.cnts)
        Up, Rig = self.UpRight_vec_gen(left_cam)
        right_cam = self.right_cam_gen(left_cam, Rig)
        return left_cam, Up, Rig, right_cam

    def cam_random_pose(self):
        left_cam = pg.CamRandomPos(self.look, self.dist, self.cnts)
        Up, Rig = self.UpRight_vec_gen(left_cam)
        right_cam = self.right_cam_gen(left_cam, Rig)
        return left_cam, Up, Rig, right_cam

    def pov_gen(self, flag=0):
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
        direc_pos = (0, 0, self.focal)
        direc_neg = (0, 0, -self.focal)

        if flag == 0:
            left_cam, up, rig, right_cam = self.cam_circle_pose()
        else:
            left_cam, up, rig, right_cam = []

            # cameras = self.cam_random_pose(self.look, self.dist, self.cnts)
        rt_list = []

        for i in range(0, self.cnts):
            # set out put name
            pov_out_name = '{:06d}'.format(i) + '.pov'
            if left_cam[i][2] < 0:
                direction = direc_pos
            else:
                direction = direc_neg
            # Write left cam
            pg.GenPovFile(self.template, left_cam[i], direction, self.look,
                          up[i], rig[i], self.povleft, pov_out_name)
            # Write right cam
            rig_look = self.look + rig[i] / int(self.ratio[0]) * 1000 * self.baseline
            pg.GenPovFile(self.template, right_cam[i], direction, rig_look,
                          up[i], rig[i], self.povright, pov_out_name)
        # save rt_list to image dir
        for i in range(0, self.cnts):
            rt = pg.SinglePoseTrans(left_cam[i], self.look, rig[i])
            rt_list.append(rt)
        # Write rt parameter
        pg.save_rt_paras(rt_list, self.imgdir+"/Camerapose.txt")

    def img_gen(self):
        pov_list = sorted(fnmatch.filter(os.listdir(self.povleft), "*.pov"))
        for pov_file in pov_list:
            img_file = pov_file[0:6] + ".png"
            # Write left img
            pg.PovToImg(
                self.povleft + "/" + pov_file,
                self.imgleft + "/" + img_file)
            # Write right img
            pg.PovToImg(
                self.povright + "/" + pov_file,
                self.imgright + "/" + img_file)

# test


if __name__ == '__main__':
    pipeline("", 0.003, "/home/lab/workspace/povtest/mve_result/stereo")
