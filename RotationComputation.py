"""chainplan Rotation Computation,"""
#2022-7-28 15:19:33 
#modified 2023-11-21 
import numpy as np
from   scipy.spatial.transform import Rotation 

EXTREME_SMALL_NUMBER_4_ROTATION_COMPUTATION = 0.00000000001

class AngularRate_and_Orientation:
    def __init__(self, initial_orientation : np.matrix, initial_omega : np.matrix, current_time):
        if initial_orientation.shape != (3, 3):
            raise ValueError("initial_orientation in AngularRate_and_Orientation must be a 3x3 matrix.")
        if initial_omega.shape != (3, 1):
            raise ValueError("initial_omega in AngularRate_and_Orientation must be a 3x3 matrix.")
        self. orientation = initial_orientation
        self. omega = initial_omega
        self. last_update_time = current_time
    
    def hat_map(self, R3vector):
    ## from R^3 → a 3x3 skew-symmetric matrix
        so3matrix = np.matrix([[0.0,            -R3vector[2,0],  R3vector[1,0]],
                              [R3vector[2,0],              0.0, -R3vector[0,0]],
                              [-R3vector[1,0],   R3vector[0,0],           0.0 ]])
        return so3matrix
    
    def vee_map(self, so3matrix):
        # from so(3) → R^3, well, is the inverst of the hat_map
        R3vector = np.matrix([[ 0.5 * ( so3matrix[2,1] - so3matrix[1,2]) ],
                              [ 0.5 * ( so3matrix[0,2] - so3matrix[2,0]) ],
                              [ 0.5 * ( so3matrix[1,0] - so3matrix[0,1])]])
        return R3vector
        
    def march_forward_with_newAngularRate(self, newAngularRate:np.matrix, current_time):
        if newAngularRate.shape != (3, 1):
            raise ValueError("newAngularRate in AngularRate_and_Orientation.march_forward_with_newAngularRate must be a 3x3 matrix.")
        gap = current_time - self. last_update_time
        self. last_update_time = current_time
        self. orientation = self. orientation + gap * self. orientation * self. hat_map(self. omega) 
    # the normalization follows mahony
        R_x = np.matrix([[ self. orientation[0,0]],
                     [ self. orientation[1,0]],
                     [ self. orientation[2,0]]])
        R_y = np.matrix([[ self. orientation[0,1]],
                     [ self. orientation[1,1]],
                     [ self. orientation[2,1]]])
        error_m = R_x.T * R_y
        error   = error_m[0,0]
        R_x_new = R_x - 0.5 * error * R_y
        R_x_new = R_x_new / (np.linalg.norm(R_x_new) + EXTREME_SMALL_NUMBER_4_ROTATION_COMPUTATION)
        R_y_new = R_y - 0.5 * error * R_x
        R_y_new = R_y_new / (np.linalg.norm(R_y_new) + EXTREME_SMALL_NUMBER_4_ROTATION_COMPUTATION)
        R_z_new_array = np.cross(R_x_new.T, R_y_new.T)
        R_z_new = np.mat([[R_z_new_array[0,0]],[R_z_new_array[0,1]],[R_z_new_array[0,2]]])
        self. orientation = np.bmat('R_x_new, R_y_new, R_z_new')
        self. omega       = newAngularRate
        
    def march_forward_with_newOrientation(self, newOrientation:np.matrix, current_time):
        if newOrientation.shape != (3, 3):
            raise ValueError("newOrientation in AngularRate_and_Orientation.march_forward_with_newAngularRate must be a 3x3 matrix.")
        gap = current_time - self. last_update_time
        self. last_update_time = current_time
        skew_symmetic = newOrientation * self. orientation. T
        self. omega = self. vee_map(skew_symmetic) / gap
        self. orientation = newOrientation

def FromMatrix2Euler_Angle_in_Rad (Rot_mat:np.matrix):
    myRotation= Rotation.from_matrix(Rot_mat)               
    return np.matrix(myRotation.as_euler('xyz', degrees=False)).T

def FromEuler_Angle_in_Rad2Matrix (Euler_Vec):
    if type(Euler_Vec) == np.matrix:
        myRotation = Rotation.from_euler('xyz', [[Euler_Vec[0,0], Euler_Vec[1,0], Euler_Vec[2,0]]], degrees=False)              
        return np.matrix(myRotation.as_matrix())
    if type(Euler_Vec) == list or type(Euler_Vec) == np.array:
        myRotation = Rotation.from_euler('xyz', [[Euler_Vec[0], Euler_Vec[1], Euler_Vec[2]]], degrees=False)              
        return np.matrix(myRotation.as_matrix())
    
def FromQuat2Euler_Angle_in_Rad(Quat_Vec):
    if type(Quat_Vec) == np.matrix:
        myRotation = Rotation.from_quat([Quat_Vec[0,0], \
                                         Quat_Vec[1,0], \
                                         Quat_Vec[2,0], \
                                         Quat_Vec[3,0]])
        return np.matrix(myRotation.as_euler('xyz'))
    if type(Quat_Vec) == list:
        if np.linalg.norm(Quat_Vec) <= 0.5:
            Quat_Vec = [0, 0, 0, 1]
        try:
            myRotation = Rotation.from_quat(Quat_Vec)
            return myRotation.as_euler('xyz')
        except:
            return np.array([0,0,0])
        



