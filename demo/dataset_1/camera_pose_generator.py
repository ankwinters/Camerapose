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
from math import sin, cos, acos, sqrt

def normalize(v, tolerance=0.00001):
    mag2 = sum(n * n for n in v)
    if abs(mag2 - 1.0) > tolerance:
        mag = sqrt(mag2)
        v = tuple(n / mag for n in v)
    return np.array(v)

class Quaternion:

    def from_axisangle(theta, v):
        theta = theta
        v = normalize(v)

        new_quaternion = Quaternion()
        new_quaternion._axisangle_to_q(theta, v)
        return new_quaternion

    def from_value(value):
        new_quaternion = Quaternion()
        new_quaternion._val = value
        return new_quaternion

    def _axisangle_to_q(self, theta, v):
        x = v[0]
        y = v[1]
        z = v[2]

        w = cos(theta/2.)
        x = x * sin(theta/2.)
        y = y * sin(theta/2.)
        z = z * sin(theta/2.)

        self._val = np.array([w, x, y, z])

    def __mul__(self, b):

        if isinstance(b, Quaternion):
            return self._multiply_with_quaternion(b)
        elif isinstance(b, (list, tuple, np.ndarray)):
            if len(b) != 3:
                raise Exception("Input vector has invalid length"+str(len(b)))
            return self._multiply_with_vector(b)
        else:
            raise Exception("Multiplication with unknown type"+str(type(b)))

    def _multiply_with_quaternion(self, q2):
        w1, x1, y1, z1 = self._val
        w2, x2, y2, z2 = q2._val
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2

        result = Quaternion.from_value(np.array((w, x, y, z)))
        return result

    def _multiply_with_vector(self, v):
        q2 = Quaternion.from_value(np.append((0.0), v))
        return (self * q2 * self.get_conjugate())._val[1:]

    def get_conjugate(self):
        w, x, y, z = self._val
        result = Quaternion.from_value(np.array((w, -x, -y, -z)))
        return result

    def __repr__(self):
        theta, v = self.get_axisangle()
        return "((%.6f; %.6f, %.6f, %.6f))"%(theta, v[0], v[1], v[2])

    def get_axisangle(self):
        w, v = self._val[0], self._val[1:]
        theta = acos(w) * 2.0

        return theta, normalize(v)

    def tolist(self):
        return self._val.tolist()

    def vector_norm(self):
        w, v = self.get_axisangle()
        return np.linalg.norm(v)


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
    _z = np.array(loc)-np.array(look_at)
    _x = np.array(right)
# Normalize
    cam_z = _z/np.sqrt(_z.dot(_z))
    cam_x = _x/np.sqrt(_x.dot(_x))
# Left-handed
    cam_y = -np.cross(cam_z,cam_x)
#    if(tuple(cam_y)[0]==0 and tuple(cam_y)[2]==0):
# Step1: rotate around world x-axis
     

if __name__=="__main__":
    cam = CamCircleLocation((0,0,0),2,6)
    DeterminRight(cam[0],(0,0,0))
