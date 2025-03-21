
import numpy as np


class Sphere:
    radius_: float
    center_: np.ndarray

    def __init__(self, radius, center):
        self.radius_ = radius
        self.center_ = center

    @property
    def radius(self):
        return self.radius_

    @property
    def center(self):
        return self.center_


class Triangle:
    vertices: np.ndarray
    normal_: np.ndarray
    area_: float

    def __init__(self, vertices):
        self.vertices = vertices

        v1 = self.vertices[1] - self.vertices[0]
        v2 = self.vertices[2] - self.vertices[0]

        self.normal_ = np.cross(v1, v2)
        self.area_ = np.linalg.norm(self.normal_) / 2

    @property
    def normal(self):
        return self.normal_

    @property
    def area(self):
        return self.area_
