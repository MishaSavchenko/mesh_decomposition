
import sys
import numpy as np
import open3d as o3d
import open3d.visualization as vis

from mesh_decomposition.data_types import Triangle, Sphere


def draw_sphere(sphere: Sphere):
    mesh = o3d.geometry.TriangleMesh.create_sphere(
        radius=sphere.radius, resolution=10)
    mesh.translate(sphere.center, relative=False)
    ev = o3d.visualization.ExternalVisualizer()
    ev.set(obj=mesh, path="sphere")


def draw_triangle(triangle: Triangle):
    mesh = o3d.geometry.TriangleMesh(vertices=o3d.utility.Vector3dVector(triangle.vertices),
                                     triangles=o3d.utility.Vector3iVector([[0, 1, 2]]))
    ev = o3d.visualization.ExternalVisualizer()
    ev.set(obj=mesh, path="triangle")
