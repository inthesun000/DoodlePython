import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.patches import Arrow
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
'''
Separation axis theorem
# site about : http://www.dyn4j.org/2010/01/sat/
'''
def normalize(v):
    from math import sqrt
    norm = sqrt(v[0] ** 2 + v[1] **2)
    return (v[0]/norm, v[1]/norm)

def orthogonal(v):
    return (-v[1], v[0])

def mul(v2, s):
    return (v2[0] * s, v2[1]*s)

def dot(x1, x2):
    return x1[0] * x2[0] + x1[1] * x2[1]

def cross(v1, v2):
    return v1[0]*v2[1] - v1[1]*v2[0]

def projection(verties, axis):
    dots = [dot(vertex, axis) for vertex in verties]
    return (min(dots), max(dots))

def length(v):
    from math import sqrt
    return sqrt(v[0]**2 + v[1]**2)

def contains(n, _range):
    a = _range[0]
    b = _range[1]
    if b < a:
        a = _range[1]
        b = _range[0]
    return (n >= a) and (n <= b)

def overlap(a,b):
    if contains(a[0], b):
        return True
    if contains(a[1], b):
        return True
    if contains(b[0], a):
        return True
    if contains(b[1], a):
        return True
    return False

def drawLine(pos, direction, c, a):
    canvas = plt.gca()
    arrow = Arrow(pos[0], pos[1], direction[0], direction[1], 0.1, color=c, alpha=a)
    canvas.add_patch(arrow)
    return arrow

def drawTargetToTargetLine(pos, targetPos, c, a):
    canvas = plt.gca()
    dirV = targetPos - pos
    arrow = Arrow(pos[0], pos[1], dirV[0], dirV[1], 0.1, color=c, alpha=a)
    canvas.add_patch(arrow)
    return arrow

def getTranslate(position, direction, size):
    return position + mul(direction, size)

# reference https://bowbowbow.tistory.com/17
def intersectPoint(p1, p2, p3, p4):
    det = cross((p2-p1),(p4-p3))
    return p1+(p2-p1)*(cross((p3-p1),(p4-p3))/det)

def getCenter(verties):
    cen = [0,0]
    for v in verties:
       cen += v
    cen = cen / len(verties)
    return cen

def getAxis(points, n, size):
    axis = []
    arrows = []
    edges = []
    for i in range(len(points)):
        j = i+1
        if j > (len(points)-1) : j = j%(len(points))
        edge = normalize(points[j] - points[i])
        normal = orthogonal(edge)
        axis.append(normal)
        # draw edge and long edge
        k = i+2
        if k > (len(points)-1) : k = k%(len(points))

        projectionJ = points[j] + mul(edge,size)
        projectionK = points[k] + mul(edge,size)

        orthogonalMin = getTranslate(projectionJ, normal, 100)
        orthogonalMax = getTranslate(projectionJ, normal, -100)    
        
        # draw Axis
        edges.append(edge)
        drawTargetToTargetLine(orthogonalMin, orthogonalMax, c=[0.2, 0.3*n, 0.5*n], a=0.6)
        arrows.append([orthogonalMin, orthogonalMax])
    return axis, arrows, edges

def getProjectionMinMaxVertex(verties, axis):
    minPos = verties[0]
    maxPos = verties[0]
    
    mindata = dot(verties[0], axis);
    maxdata = dot(verties[0], axis);
    for i in range(len(verties)):
        if mindata < dot(verties[i],axis) :
            minPos = verties[i]
            mindata = dot(verties[i],axis)
        if maxdata > dot(verties[i], axis) :
            maxPos = verties[i]
            maxdata = dot(verties[i],axis)

    return minPos, maxPos    

def drawLineOnAxis(verteis, axis, edge, arrowMinMax, c):
    minV1, maxV1 = getProjectionMinMaxVertex(verteis, axis)
       
    v1 = getTranslate(minV1, edge, 100)
    v2 = getTranslate(maxV1, edge, 100)

    intersectP1 = intersectPoint(minV1, v1, arrowMinMax[0], arrowMinMax[1])
    intersectP2 = intersectPoint(maxV1, v2, arrowMinMax[0], arrowMinMax[1])

    drawTargetToTargetLine(intersectP1, intersectP2, c, a=0.5)
    drawTargetToTargetLine(minV1, intersectP1, c=[0.2,0.5,0], a=0.2)
    drawTargetToTargetLine(maxV1, intersectP2, c=[0.4,0,1], a=0.2)
    

def SAT(vertiesA, vertiesB):
    center1 = getCenter(vertiesA)
    center2 = getCenter(vertiesB)

    center = center2 - center1
    lenC = length(center) + 2
    
    axis1, arrows1, edges1 = getAxis(vertiesA, 1, lenC)
    axis2, arrows2, edges2 = getAxis(vertiesB, 2, lenC)
    axes = axis1 + axis2
    arrows = arrows1 + arrows2
    edges = edges1 + edges2
    
    for i in range(len(axes)):
        drawLineOnAxis(vertiesA, axes[i], edges[i], arrows[i], c=[1,0,0])
        drawLineOnAxis(vertiesB, axes[i], edges[i], arrows[i], c=[0,1,0])
      
        p1 = projection(vertiesA, axes[i])
        p2 = projection(vertiesB, axes[i])
        overlapping = overlap(p1, p2)
        if not overlapping:
            axisLine = arrows[i]
            drawTargetToTargetLine(axisLine[0], axisLine[1], c=[1,0,1], a=1)
            print(axisLine)
            return False       
    return True


#Setting figure and grid
fig = plt.figure("Separation Axis theorem")
ax = fig.add_subplot(1, 1, 1)
fig.set_size_inches(8, 8)
w = 30
h = 30
ax.set_xlim(-w,w)
ax.set_ylim(-h,h)

ax.xaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_major_locator(MultipleLocator(10))

ax.xaxis.set_minor_locator(AutoMinorLocator(10))
ax.yaxis.set_minor_locator(AutoMinorLocator(10))

ax.grid(which='major', color='#CCCCCC', linestyle=':',alpha=0.8)
ax.grid(which='minor', color='#CCCCCC', linestyle=':', alpha=0.5)

plt.grid(True)


#Shape and SAT

#case 1 : don't collide
vertexPoints1 = np.array([[2,2], [6,5], [3,6]])
vertexPoints2 = np.array([[6,7], [6,10], [8,14], [10,10]])
#case 2 : collide
#vertexPoints1 = np.array([[2,6], [3,0], [7,6]])
#vertexPoints2 = np.array([[10,10], [9,2], [5,8]])

shape1 = Polygon(vertexPoints1, closed=True, fill=False, color=[0.5,0.3,0.0])
shape2 = Polygon(vertexPoints2, closed=True, fill=False, color=[0.5,0.2,0.5])
ax.add_patch(shape1)
ax.add_patch(shape2)

overlap = SAT(vertexPoints1, vertexPoints2)
print(overlap)

plt.show() 
