#!/usr/bin/env python3
from camera_pose_generator import GenCams
from stereo_cam_pose_generator import Stereo
import os


def ClearFiles(dst_dir):
    pov_out_dir = dst_dir + "/pov_files"
    img_out_dir = dst_dir + "/img_files"
    pose_file = dst_dir + "/Camerapose.txt"
    valid_file = dst_dir + "/validCamerapose.txt"
    os.system("rm -f " + pov_out_dir + "/*.pov")
    os.system("rm -f " + img_out_dir + "/*.png")
    os.system("rm " + pose_file)
    os.system("rm " + valid_file)


def pipeline(dist, focal, dst_dir):
    ClearFiles(dst_dir)
# test
    GenCams("./gt.pov", dst_dir, pose_file="Camerapose.txt", pov_dir_name="pov_files", img_dir_name="img_files",
            # flag=0,file_counts=8,distance=dist,look_at=(0,0.7,0),focal_len=focal/1000)
            flag=0, file_counts=360, distance=dist, look_at=(0, 0.7, 0), focal_len=focal / 1000)
    os.system("cp -r " + dst_dir + " ../../mve_result/gt%02dm" % dist)


def GenReconstruct(dst_dir):
    pipeline(3, 5, dst_dir)
    for i in range(4, 6):
        pipeline(i, 7.5, dst_dir)
    for i in range(6, 8):
        pipeline(i, 10, dst_dir)
    for i in range(8, 11):
        pipeline(i, 15, dst_dir)
    for i in range(11, 21):
        focal = 5 * (i + 1) // 2 - 10
        ClearFiles(dst_dir)
        GenCams("./gt.pov", dst_dir, pose_file="Camerapose.txt", pov_dir_name="pov_files", img_dir_name="img_files",
                flag=0, file_counts=360, distance=i, look_at=(0, 0.7, 0), focal_len=focal / 1000)
        os.system("cp -r " + dst_dir + " ../../mve_result/gt%02dm" % i)


def Validpipeline(dist, focal, dst_dir):
    ClearFiles(dst_dir)
    GenCams("./gt.pov", dst_dir, pose_file="validCamerapose.txt", pov_dir_name="pov_files", img_dir_name="img_files",
            flag=1, file_counts=20, distance=dist, look_at=(0, 0.7, 0), focal_len=focal / 1000)
    os.system("cp -r " + dst_dir + " ../../mve_result/gt%02dm_valid" % dist)


def GenValidation(dst_dir):
    Validpipeline(3, 5, dst_dir)
    for i in range(8, 11):
        Validpipeline(i, 15, dst_dir)
    for i in range(6, 8):
        Validpipeline(i, 10, dst_dir)
    for i in range(4, 6):
        Validpipeline(i, 7.5, dst_dir)
    for i in range(11, 21):
        focal = 5 * (i + 1) // 2 - 10
        ClearFiles(dst_dir)
        GenCams("./gt.pov", dst_dir, pose_file="validCamerapose.txt", pov_dir_name="pov_files", img_dir_name="img_files",
                flag=1, file_counts=20, distance=i, look_at=(0, 0.7, 0), focal_len=focal / 1000)
        os.system("cp -r " + dst_dir + " ../../mve_result/gt%02dm_valid" % i)


def test():
    pipeline(3, 5, "./mono3m")
    Validpipeline(3, 5, "./mono3m/valid")

class mono_pipe:
    pass

class stereo_pipe_example:
    def __init__(self, template_dir, dst_dir, work_dir="/tmp"):
        # temperory
        self.currentdir = os.path.abspath(os.curdir)
        # Initialize
        self.template_dir = os.path.abspath(template_dir)
        self.dst_dir = os.path.abspath(dst_dir)
        self.work_dir = os.path.abspath(work_dir)
        os.chdir(self.template_dir)

    def __del__(self):
        os.chdir(self.currentdir)

    def pipeline(self, dist, focal, pipeflag=0):
        template_file = self.template_dir+"/gt.pov"
        if pipeflag == 0:
            files = 360
            output_dir = self.dst_dir+"/gt%02ds" % dist
        else:
            files = 20
            output_dir = self.dst_dir+"/gt%02ds_valid" % dist
        example = Stereo(template_file, self.work_dir, baseline=0.10, file_counts=files,
                         distance=dist, look_at=(0, 0.7, 0), focal_len=focal, ratio=(4, 3))
        example.pov_gen(flag=pipeflag)
        example.img_gen()
        os.system("cp -r "+example.imgdir+" "+output_dir)

    def reconstruct_gen(self):
        # distance = 2m, focal = 3 mm
        self.pipeline(2, 3 / 1000)
        """
        self.pipeline(3, 5 / 1000)
        for i in range(4, 6):
            self.pipeline(i, 7.5 / 1000)
        for i in range(6, 8):
            self.pipeline(i, 10 / 1000)
        for i in range(8, 11):
            self.pipeline(i, 15 / 1000)
        for i in range(11, 21):
            f = 5 * (i + 1) // 2 - 10
            self.pipeline(dist=i, focal=f)
        """

    def valid_gen(self):

        valid_flag = 1
        self.pipeline(2, 3 / 1000, valid_flag)
        """
        self.pipeline(3, 5 / 1000, valid_flag)
        for i in range(4, 6):
            self.pipeline(i, 7.5 / 1000, valid_flag)
        for i in range(6, 8):
            self.pipeline(i, 10 / 1000, valid_flag)
        for i in range(8, 11):
            self.pipeline(i, 15 / 1000, valid_flag)
        for i in range(11, 21):
            f = 5 * (i + 1) // 2 - 10
            self.pipeline(dist=i, focal=f, valid_flag)
        """

if __name__ == '__main__':
    # pipeline(2,3,"./mono3m")
    #dst = "./mono3m/valid"
    # Validpipeline(2,3,dst)

    #GenReconstruct("./mono3m")
    #GenValidation(dst)
    gt02s = stereo_pipe_example("./template", "/home/lab/workspace/povtest/mve_result", "./mono3m")
    gt02s.reconstruct_gen()
