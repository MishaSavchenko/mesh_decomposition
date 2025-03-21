
from mesh_decomposition.data_types import Triangle, Sphere
from mesh_decomposition.visualizer.client_utils import *


radius = 1
center = np.array([0.0, 0.0, -1.0])
s = Sphere(radius=1, center=center)


z = 0
vertices = np.array([[-1.0, -1.0, z],
                     [-1.0, 1.0, z],
                     [1.0, 1.0, z-1.0]])
t = Triangle(vertices)

draw_triangle(t)

draw_sphere(s)
