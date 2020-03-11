'''
auther: kejun
data  : 2020-03-10
'''

import math
from matplotlib import pyplot as plt 
import numpy as np



'''
func: normalize the angle into [0 2pi]
'''
def normalize_angle_2pi(angle):
    if angle > (math.pi*2):
        return angle-math.pi*2
    elif angle < 0:
        return angle+math.pi*2
    else:
        return angle

'''
func: coordiante transfor matrix 
heading: start heading of line
'''
def gen_rotate_matrix(heading):
    theta = math.pi*0.5-heading # if heading is related to y axis, need do this
                                # if heading is related to x axis, need del this
    return np.array([[math.cos(theta), math.sin(theta)],
                     [-math.sin(theta), math.cos(theta)]])


def gen_translation_matrix(x, y):
    return np.array([x, y])


def get_arc_points(length, curvature):
    r = 1.0/curvature
    delta_theta = 5.0/180.0*math.pi
    theta = 0
    point_set = np.zeros([0,2], dtype='float64')
    headings = []
    while theta <= length/r:
        x = r*math.sin(theta)
        y = r*(1-math.cos(theta))
        heading = theta
        headings.append(heading)
        point_set = np.insert(point_set, point_set.shape[0], [x, y], 0)
        theta = theta + delta_theta
    return point_set, headings



'''
func: points offset
ori_points_set: input points
point_headings: every point heading of ori_points_set
is_left: transfor direction
d: transfor distance
'''
def point_offset(ori_points_set, point_headings, is_left, d):
    result_point_set = np.zeros([0,2])

    for i in range(ori_points_set.shape[0]):
    #for heading in point_headings:
        heading = point_headings[i]
        if is_left:
            transfor_angle = heading + math.pi*0.5
        else:
            transfor_angle = heading - math.pi*0.5
        transfor_angle = normalize_angle_2pi(transfor_angle)
        transfor_vector = np.array([d*math.cos(transfor_angle), d*math.sin(transfor_angle)], dtype='float64')
        #print("transfor_vector: ",heading, transfor_angle, transfor_vector[0], transfor_vector[1])
        point = ori_points_set[i]
        point = point + transfor_vector
        result_point_set = np.insert(result_point_set, result_point_set.shape[0], point, 0)
    
    return result_point_set

'''
func: point coordinate transfor
point_set: original points of line
ori_x, ori_y: start coordinate of line
ori_heading: start heading of line
'''
def point_coor_transfor(point_set, ori_x, ori_y, ori_heading):
    rotate_matrix = gen_rotate_matrix(ori_heading)
    translation_matrix = gen_translation_matrix(ori_x, ori_y)
    point_set = point_set.dot(rotate_matrix)
    point_set = np.add(point_set,translation_matrix)
    return point_set



if __name__ == '__main__':
    x = 25
    y = 25
    length = 10
    curvature = 0.2
    d = 1
    is_left = False
    headings = np.linspace(0.0, 360.0/180.0*math.pi, num=9)
    #headings = []
    #headings.append(90.0/180.0*math.pi)
    for heading in headings:
        print("heading ", heading)
        #line_transfor(x, y, heading, length, d, is_left)
        ori_points, points_headings = get_arc_points(length, curvature)
        result_points = point_offset(ori_points, points_headings, is_left, d)
        ori_points = point_coor_transfor(ori_points, x, y, heading)
        result_points = point_coor_transfor(result_points, x, y, heading)
        print("ori point num", ori_points.shape[0])
        #print("result point num", result_points.shape[0])
        #plt.cla()
        plt.xlim((0,50))
        plt.ylim((0,50))
        plt.plot(ori_points[:,0], ori_points[:,1], '')
        plt.pause(0.2)
        plt.plot(result_points[:,0], result_points[:,1],'')
        plt.pause(0.2)
    plt.show()   
    
    
    