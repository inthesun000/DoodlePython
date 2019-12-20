import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.patches import Arrow

def AddEdge(points):
    canvas = plt.gca()
    for i in range(len(points)):
        j = i+1
        if j > (len(points)-1) : j = 0
        edge = points[i] - points[j]
        #normal = [-y, x]
        normal = [-edge[1], edge[0]]
        pos = points[j] + (edge * 0.5)
        arrow = Arrow(pos[0], pos[1], normal[0], normal[1], 0.1, color=[0.98, 0.78, 0])
        canvas.add_patch(arrow)

def TestEdge(points):
    print(len(points))
    for i in range(len(points)):
        print(i)
        
    
ax = plt.gca()
w = 50
h = 50
ax.set_xlim(0,w)
ax.set_ylim(0,h)
        
vertexPoints = np.array([[2,2], [6,5], [3,6]])

p = Polygon(vertexPoints, closed=True, fill=False)
ax.add_patch(p)

#TestEdge(vertexPoints)
AddEdge(vertexPoints)

plt.show()
