# import trimesh
# import coacd

# input_file = "/home/misha/code/mesh_decomposition/assets/cup.fbx"
# input_file = "/home/misha/code/mesh_decomposition/assets/Round_Stand.obj"
# mesh = trimesh.load(input_file, force="mesh")
# mesh = coacd.Mesh(mesh.vertices, mesh.faces)
# parts = coacd.run_coacd(mesh) # a list of convex hulls.

# Minimize using a variant of the Lloyd clustering algorithm.
# discretize the object into a set of points including points on its surface adn within its interior.
# bind each one of the clusters with a sphere
# Clusting Iteration:
from mesh_decomposition.visualizer.client_utils import *
from mesh_decomposition import *
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from mesh_decomposition.data_types import Triangle, Sphere

# point assignment to clusters
# cluster sphere update
# cluster teleportation until error converges

# Preprocessing

# inner and surface points
# inner point are generated by voxelizing the object into a regular grid and eliminating grid points outside the object
# manual grid size selection
# points on the mesh surface are generated by sorting triangles by their areas and sampling randomly in proportion to these areas
#
# points are combined into volumentic representation to be partitioned in clustering


# Point Assignment
# choose random inner points for the sphere centers and set their radii to 0
# a point is assigned to the cluster it is closest to based on outside volume
# cluster's bounding sphere raidus is enlarged in order to include a point
# once enlarged, sphere outside volume is computed
# point is assigned to that cluster whose outside volume increases least
# in case of a tie p is assigned to the cluser whose sphere center is closest


#  4 possible relationships between a sphere and a triangle
# Volume bound by spherical triangle formed by project the vertices of triangle onto the sphere
def Vstri(triangle, sphere):
    #
    pass
# Volume of the tetrahedron formed by the sphere center and the three vertices of the triangle


def Vtet(triangle, sphere_center):
    pass


def SOTV_(triangle, sphere):
    return Vstri(triangle, sphere) - Vtet(triangle, sphere.center)


def triangle_height_over_sphere(triangle: Triangle,
                                sphere: Sphere):
    v = triangle.vertices[0] - sphere.center
    n = triangle.normal / np.linalg.norm(triangle.normal)
    return np.abs(np.dot(v, n))


# 3 vert. in
def SOTV_a(triangle: Triangle, sphere: Sphere):
    # solid angle of the triangle on the sphere
    omega = triangle.area / (sphere.radius ** 2)
    # area of the triangle
    D = triangle.area
    # height of the the triangle plane about center of the sphere
    h = triangle_height_over_sphere(triangle, sphere)
    r = sphere.radius
    return 1.0 / 3.0 * ((r ** 3) * omega - D * h)
    # return Vstri(triangle, sphere) - Vtet(triangle, sphere.center)


# 3 vert. out
def SOTV_b(triangle: Triangle, sphere: Sphere):
    h = triangle_height_over_sphere(triangle, sphere)
    return np.pi * h ** 2 * (sphere.radius - h / 3.0)


radius = 1.5
center = np.array([0.0, 0.0, -1.0])
s = Sphere(radius=1, center=center)

z = 10.0

vertices = np.array([[-1.0, -1.0, z],
                     [-1.0, 1.0, z],
                     [0.5, 0.5, z-1.0]])
t = Triangle(vertices)

res = triangle_height_over_sphere(t, s)


# print("height over sphere :", res)
# print("SOTV :", SOTV_a(t, s))


# for case (c),
# we find the arc representing the intersection of the triangle and sphere, and the two points,
# p0 and p1, where this arc intersects the triangle edges (green points in Figure 3c, bottom).
# The outside volume can be further decomposed into one volume correspond ing to case (a)
# and an additional “swing” volume whose computation we will describe in more detail later.
def SOTV_c(triangle: Triangle, sphere: Sphere):
    # find the the closes point of the triangle to the center of the sphere

    indx = np.argmin(np.linalg.norm(triangle.vertices - sphere.center, axis=1))

    p0 = triangle.vertices[indx]

    if indx == 0:
        p1, p2 = triangle.vertices[1], triangle.vertices[2]
    elif indx == 1:
        p1, p2 = triangle.vertices[0], triangle.vertices[2]
    else:
        p1, p2 = triangle.vertices[0], triangle.vertices[1]

    v1 = p1 - p0
    v2 = p2 - p0

    # a = (xB-xA)²+(yB-yA)²+(zB-zA)²
    a = np.linalg.norm(v1) ** 2
    # b = 2*((xB-xA)(xA-xC)+(yB-yA)(yA-yC)+(zB-zA)(zA-zC))
    b = 2 * (p2 - p1) * (p1 - sphere.center)
    # c = (xA-xC)²+(yA-yC)²+(zA-zC)²-r²
    c = np.linalg.norm(p0 - sphere.center) ** 2 - sphere.radius ** 2
    Delta = b ** 2 - 4 * a * c

    print(v1, v2)
    print(c)
    print(Delta)
    # # print(p0)
    # # print(sphere.center)
    # # print(p2 - p1)
    # # print(p1 - sphere.center)
    # print()

    # # v1 =
    # d0 = np.linalg.norm(triangle.vertices[0] - sphere.center)
    # d1 = np.linalg.norm(triangle.vertices[1] - sphere.center)
    # d2 = np.linalg.norm(triangle.vertices[2] - sphere.center)

    # p0 =
    # SOTV_a()
    pass


draw_triangle(t)
draw_sphere(s)

SOTV_c(t, s)
