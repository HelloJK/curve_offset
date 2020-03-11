'''
auther: kejun
data  : 2020-03-10
reference: https://blog.csdn.net/qq_30816923/article/details/100768654
'''

import math
import numpy as np
from matplotlib import pyplot as plt


'''
func: get coordinate of distance point
curveStart: start curvature
curveEnd: end curvature
curveLength: total length of curve
distance: distance from start point
return: the coordinate of distance point
'''
def clothoid(curveStart, curveEnd, curveLength, distance):
    A = (curveEnd - curveStart) / curveLength
    s0 = curveStart / A
    X0, Y0 = clothoid_coordinate(A, s0)
    heading0 = A / 2 * s0 ** 2
    transferMatrix = np.linalg.inv(transfor_coordinate(heading0))
    X, Y = clothoid_coordinate(A, distance + s0)
    local = np.dot(transferMatrix, np.array([[X], [Y]]) - np.array([[X0], [Y0]]))
    x = local[0, 0]
    y = local[1, 0]
    heading = A / 2 * distance ** 2 + curveStart * distance
    return x, y, heading, math.cos(heading), math.sin(heading)


def clothoid_coordinate(A, distance):
    x = 0.0
    y = 0.0
    for n in range(30):
        x += math.pow(-1, n) * math.pow(A, 2 * n) * math.pow(distance, 4 * n + 1) / \
             (math.factorial(2 * n) * (4 * n + 1) * math.pow(2, 2 * n))
        y += math.pow(-1, n) * math.pow(A, 2 * n + 1) * math.pow(distance, 4 * n + 3) / \
             (math.factorial(2 * n + 1) * (4 * n + 3) * math.pow(2, 2 * n + 1))
    return x, y

'''
func: coordiante transfor matrix 
'''
def transfor_coordinate(heading):
    return np.array([[math.cos(heading), -math.sin(heading)],
                     [math.sin(heading), math.cos(heading)]])


if __name__=="__main__":
    curStart = 0 # start curv
    curEnd = 0.12698412698412698  # end curv
    n = 30 # step num
    l2 = 4*n + 1
    l3= math.pow(10, 300/(4*n+1))
    lk0 = min(2*math.pow(math.factorial(2*n), 1 / (2*n))/abs(curStart + 1e-5), l2, l3)
    lkt = min(2*math.pow(math.factorial(2*n), 1 / (2*n))/abs(curEnd + 1e-5), l2, l3)
    
    allowsCurveLength = abs(lk0+lkt) if curEnd*curStart<=0 else abs(lkt-lk0)
    print("The allowed curve length is {}".format(allowsCurveLength))
    
    curveLength = 9.1954178989066371
    print("The given curve length is {}".format(curveLength))

    x = []
    y = []
    heading = []
    distance = np.linspace(0, curveLength, 1000)
    for i in distance:
        X, Y, Heading, W, D = clothoid(curStart, curEnd, curveLength, i)
        x.append(X)
        y.append(Y)
        heading.append(Heading)
    plt.plot(x, y)
    plt.show()

