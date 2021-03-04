'''
Created on 23 Jan 2015

@author: Kristjan
'''

from fem.geometry import Geometry
from fem.mesh import Mesh
from fem.setup import Setup

import matplotlib.pyplot as plt

class Controller(object):
    
    def __init__(self):
        self.geometry = Geometry()
    
    def draw_geom(self):
        self.geometry.draw()
        plt.show()
    
    def reset_geom(self, xmin, xmax, ymin, ymax):
        self.geometry = Geometry(xmin, xmax, ymin, ymax)
    
    def generate_mesh(self, xstep, ystep):
        self.mesh = Mesh(self.geometry, xstep, ystep)
        self.mesh.generate_mesh()
    
    def draw_mesh(self, nodes_only):
        self.mesh.draw(nodes_only)
        axes = plt.gca()
        self.geometry.draw()
        axes.set_xlim([self.geometry.x_min, self.geometry.x_max])
        axes.set_ylim([self.geometry.y_min, self.geometry.y_max])
        plt.show()
    
    def solve(self, geom_type, method_index):
        self.setup = Setup(self.mesh)
        self.setup.init_system_mat(geom_type)
        self.setup.boundary_conditions()
        self.setup.solve(method_index)
    
    def draw_solution(self, with_nodes, with_geom):
        if with_geom:
            self.geometry.draw()
        if with_nodes:
            self.mesh.draw(1)
        self.setup.draw()
        axes = plt.gca()
        axes.set_xlim([self.geometry.x_min, self.geometry.x_max])
        axes.set_ylim([self.geometry.y_min, self.geometry.y_max])
        plt.show()
    
    def probe_value(self, x, y):
        return self.setup.probe_u(x, y)
    
    def start(self):
        
        self.geometry.add_circular(-20, 0, 10, 1)
        #geom.add_circular(50, 0, 10, 0)
        #geom.add_rectangular(-20, -40, 20, 0, 100)
        #geom.add_rectangular(30, 30, 40, 40, -50)
        #geom.add_circular(-30, 30, 10, -100)
        
        
        mesh = Mesh(self.geometry, 1.5, 1.5)
        mesh.generate_mesh()
        setup = Setup(mesh)
        setup.init_system_mat()
        setup.boundary_conditions()
        setup.solve()
        
        self.geometry.draw()
        mesh.draw(1)
        setup.draw()
        plt.show()
