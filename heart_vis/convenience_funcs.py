#convenience_funcs.py
import numpy as np
import math
import bpy

from heart_vis.config import *

def get_scale(ctrlName, obj, maxScale, minScale, distRange):

    '''
    Function to calculate the intended scale in the driver expression, using getDistance
    '''

    ctrl = bpy.data.objects[ctrlName]
    dist = get_distance(ctrl, obj)
    power = ctrl.scale[0]
    scaleRange = maxScale - minScale
    dist = dist/power   #distance is affected by the control size as well

    if dist > distRange:
        scale = minScale
    else:
        scale = scaleRange/(distRange**2)*(dist**2) - 2*scaleRange/distRange*dist + maxScale    #Here you define your scale function

    return scale


def get_distance(ctrl, obj):

    sum = 0
    for i in range(3):
        sum += (ctrl.location[i] - obj.location[i])**2

    return sum**0.5



def rotation_matrix_from_vectors(vec1, vec2):

    '''
    Find the rotation matrix that aligns vec1 to vec2
        vec1: A 3d "source" vector
        vec2: A 3d "destination" vector
    Returns:
        mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    '''

    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

    return rotation_matrix

def rot2eul(R):

    '''
    Convert the rotation matrix R to euler rotations in x,y,z components.

    Input:
        R: ndarray; rotation matrix

    Returns:
        (alpha, beta, gamma): as a numpy array
    '''

    beta = -np.arcsin(R[2,0])
    alpha = np.arctan2(R[2,1]/np.cos(beta),R[2,2]/np.cos(beta))
    gamma = np.arctan2(R[1,0]/np.cos(beta),R[0,0]/np.cos(beta))

    return np.array((alpha, beta, gamma))

def calc_angle(point1,point2,point3):

    # Unpack the tuples
    x1 = point1[0]
    y1 = point1[1]
    z1 = point1[2]

    x2 = point2[0]
    y2 = point2[1]
    z2 = point2[2]

    x3 = point3[0]
    y3 = point3[1]
    z3 = point3[2]

    vec1 = [x2-x1, y2-y1, z2-z1]
    vec2 = [x3-x2, y3-y2, z3-z2]

    uv1 = vec1 / np.linalg.norm(vec1)
    uv2 = vec2 / np.linalg.norm(vec2)
    dot_product = np.dot(uv1,uv2)
    angle = np.arccos(dot_product)

    angle = (angle * 180) / np.pi # Find angle in degrees

    return angle
