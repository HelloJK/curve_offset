'''
auther: kejun
data  : 2020-03-10
'''

import math
import numpy as np
from matplotlib import pyplot as plt
from spiral_line import clothoid


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


'''
func: get points set of spiral line
curveStart: start curvature of spiral line
curveEnd: end curvature of spiral line
curveLength: length of spiral line
'''
def get_spiral_point(curveStart, curveEnd, CurveLength):
    point_set = np.zeros([0,2], dtype='float64')
    distance = np.linspace(0, curveLength, 50)
    headings = []
    for i in distance:
        X, Y, Heading, W, D = clothoid(curveStart, curveEnd, curveLength, i)
        point_set = np.insert(point_set, point_set.shape[0], [X,Y], 0)
        print("heading:", Heading)
        headings.append(Heading)
    return point_set, headings


if __name__=="__main__":
    curStart = 0 # start curv
    curEnd = 0.12698412698412698  # end curv    
    curveLength = 50
    start_x = 50
    start_y = 50
    is_left = False
    d = 1
    headings = np.linspace(0.0, 360.0/180.0*math.pi, num = 9)
    #headings = []
    #headings.append(0.0/180.0*math.pi)
    for heading in headings:
        ori_points, point_headings = get_spiral_point(curStart, curEnd, curveLength)
        result_points = point_offset(ori_points, point_headings, is_left, d)
        ori_points = point_coor_transfor(ori_points, start_x, start_y, heading)
        result_points = point_coor_transfor(result_points, start_x, start_y, heading)
        #print("heading: ", heading)
        #plt.cla()
        plt.plot(ori_points[:,0], ori_points[:,1], ".")
        plt.xlim((0, 100))
        plt.ylim((0, 100))
        plt.pause(0.2)
        plt.plot(result_points[:,0], result_points[:,1], ".")
    

    plt.show()
    


