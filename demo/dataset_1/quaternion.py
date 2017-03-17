#!/usr/bin/env python3
import numpy as np
from math import sin, cos, acos, sqrt, radians, degrees


def normalize(v, tolerance=0.00001):
    mag2 = sum(n * n for n in v)
    if abs(mag2 - 1.0) > tolerance and mag2 != 0:
        mag = sqrt(mag2)
        v = tuple(n / mag for n in v)
    #print("v:",v,"mag2:",mag2)
    return np.array(v)

class Quaternion:


    def from_axisangle(theta, v):
        theta = theta
        v = normalize(v)


        #print("v:",v,"theta:",theta)
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
# degrees to radians
        th = radians(theta)

        w = cos(th/2.)
        x = x * sin(th/2.)
        y = y * sin(th/2.)
        z = z * sin(th/2.)
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

    def __str__(self):
        theta, v = self.get_axisangle()
        return "((%.1f; %.6f, %.6f, %.6f))"%(theta, v[0], v[1], v[2])

    def get_axisangle(self):
        w, v = self._val[0], self._val[1:]
        th = acos(w) * 2.0
    # radians to degrees
        theta = degrees(th)

        return theta, normalize(v)

    def tolist(self):
        return self._val.tolist()

    def vector_norm(self):
        w, v = self.get_axisangle()
        return np.linalg.norm(v)
    def get_rotation_matrix(self):
        w = self._val[0]
        x = self._val[1]
        y = self._val[2]
        z = self._val[3]
        wx = w * x 
        wy = w * y
        wz = w * z
        xx = x * x
        xy = x * y
        xz = x * z
        yy = y * y
        yz = y * z
        zz = z * z
        """
        [ 1 - 2(yy + zz)         2(xy - wz)          2(xz + wy)  ]
        [      2(xy + wz)     1 - 2(xx + zz)         2(yz - wx)  ]
        [      2(xz - wy)        2(yz + wx)     1 - 2(xx + yy) ]
        """
        return np.array([ (1-2*(yy+zz),2*(xy-wz),2*(xz+wy)),
                          (2*(xy+wz),1-2*(xx+zz),2*(yz-wx)),
                          (2*(xz-wy),2*(yz+wx),1-2*(xx+yy)) ]
                          )

