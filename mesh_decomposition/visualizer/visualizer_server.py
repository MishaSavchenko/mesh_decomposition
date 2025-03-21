
import sys
import numpy as np
import open3d as o3d
import open3d.visualization as vis


def spawn_server():
    o3d.visualization.draw(title="Open3D - Remote Visualizer Client",
                           show_ui=True,
                           rpc_interface=True)


if __name__ == "__main__":
    spawn_server()
