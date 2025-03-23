import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import random
import threading
import time
import zmq
import dill

import asyncio
import zmq
from zmq.asyncio import Context


class Open3DVisualizationServer:
    MENU_SPHERE = 1
    MENU_RANDOM = 2
    MENU_QUIT = 3

    def __init__(self):
        self._id = 0
        self.window = gui.Application.instance.create_window(
            "Add Spheres Example", 1024, 768)
        self.scene = gui.SceneWidget()
        self.scene.scene = rendering.Open3DScene(self.window.renderer)
        self.scene.scene.set_background([0, 0, 0, 1])
        self.scene.scene.scene.set_sun_light(
            [-1, -1, -1],  # direction
            [1, 1, 1],  # color
            100000)  # intensity
        self.scene.scene.scene.enable_sun_light(True)
        self.scene.scene.show_axes(True)
        # self.scene.scene.show_skybox(True)
        self.scene.scene.show_ground_plane(
            True, rendering.Scene.GroundPlane(0))

        bbox = o3d.geometry.AxisAlignedBoundingBox([-5, -5, -5],
                                                   [5, 5, 5])
        self.scene.setup_camera(60, bbox, [0, 0, 0])

        self.window.add_child(self.scene)
        # The menu is global (because the macOS menu is global), so only create
        # it once, no matter how many windows are created
        if gui.Application.instance.menubar is None:

            debug_menu = gui.Menu()
            debug_menu.add_item("Add Sphere", self.MENU_SPHERE)
            debug_menu.add_item("Add Random Spheres", self.MENU_RANDOM)

            debug_menu.add_separator()
            debug_menu.add_item("Quit", self.MENU_QUIT)

            menu = gui.Menu()
            menu.add_menu("Debug", debug_menu)

            gui.Application.instance.menubar = menu

        # The menubar is global, but we need to connect the menu items to the
        # window, so that the window can call the appropriate function when the
        # menu item is activated.

        self.window.set_on_menu_item_activated(self.MENU_SPHERE,
                                               self._on_menu_sphere)

        self.window.set_on_menu_item_activated(self.MENU_RANDOM,
                                               self._on_menu_random)

        self.window.set_on_menu_item_activated(self.MENU_QUIT,
                                               self._on_menu_quit)

        self.setup_zmq_socket()

    def setup_zmq_socket(self):

        self.zmq_context = zmq.Context.instance()
        self.zmq_socket = self.zmq_context.socket(zmq.REP)
        self.zmq_socket.bind("tcp://*:5555")
        # self.zmq_socket.on_recv(self.zmq_callback)

        # ctx = Context.instance()

    # async def recv(self):
    #     s = ctx.socket(zmq.SUB)
    #     s.connect('tcp://127.0.0.1:5555')
    #     s.subscribe(b'')
    #     while True:
    #         msg = await s.recv_multipart()
    #         print('received', msg)
    #     s.close()

    def zmq_callback(self, msg):
        print("asdas")
        pass

    def add_sphere(self):
        self._id += 1
        mat = rendering.MaterialRecord()
        mat.base_color = [
            random.random(),
            random.random(),
            random.random(), 1.0
        ]
        mat.shader = "defaultLit"
        sphere = o3d.geometry.TriangleMesh.create_sphere(0.5)
        sphere.compute_vertex_normals()
        sphere.translate([
            10.0 * random.uniform(-1.0, 1.0),
            10.0 * random.uniform(-1.0, 1.0),
            10.0 * random.uniform(-1.0, 1.0)
        ])
        self.scene.scene.add_geometry("sphere" + str(self._id), sphere, mat)

    def _on_menu_sphere(self):
        # GUI callbacks happen on the main thread, so we can do everything
        # normally here.
        self.add_sphere()

    def _on_menu_random(self):
        # This adds spheres asynchronously. This pattern is useful if you have
        # data coming in from another source than user interaction.
        def thread_main():
            for _ in range(0, 20):
                # We can only modify GUI objects on the main thread, so we
                # need to post the function to call to the main thread.
                gui.Application.instance.post_to_main_thread(
                    self.window, self.add_sphere)
                time.sleep(1)
        threading.Thread(target=thread_main).start()

    def _on_menu_quit(self):
        gui.Application.instance.quit()


def main():
    gui.Application.instance.initialize()
    Open3DVisualizationServer()
    gui.Application.instance.run()


if __name__ == "__main__":
    main()
