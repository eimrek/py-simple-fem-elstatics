'''
Created on 11 Jan 2015

@author: Kristjan
'''
import numpy as np
import matplotlib.pyplot as plt
import fem.util as util

class Element(object):
    '''
    The element
    '''
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.nodes = [a, b, c]
    
    def in_elem(self, x, y):
        '''
        Checks if the point (x,y) is inside the element
        Assumes that numbering is counter-clockwise
        Also true if on the edge (> -> >=)
        '''
        p0x = self.a.x
        p0y = self.a.y
        p1x = self.b.x
        p1y = self.b.y
        p2x = self.c.x
        p2y = self.c.y
        area = 1/2*(-p1y*p2x + p0y*(-p1x + p2x) + p0x*(p1y - p2y) + p1x*p2y)
        s = 1/(2*area)*(p0y*p2x - p0x*p2y + (p2y - p0y)*x + (p0x - p2x)*y)
        t = 1/(2*area)*(p0x*p1y - p0y*p1x + (p0y - p1y)*x + (p1x - p0x)*y)
        return (s>=0 and t>=0 and 1-s-t>=0)
    
    def lin_coef(self, u):
        '''
        Returns the linear coefficients for approximating
        the potential inside the element:
        u(x,y)=alpha1+alpha2*x+alpha3*y
        '''
        coord = np.array([[1, self.a.x, self.a.y],
                          [1, self.b.x, self.b.y],
                          [1, self.c.x, self.c.y]])
        u_nodes = np.array([u[self.a.nr], u[self.b.nr], u[self.c.nr]])
        return np.linalg.inv(coord).dot(u_nodes)
    
    def draw(self):
        x = [self.a.x,self.b.x,self.c.x,self.a.x]
        y = [self.a.y,self.b.y,self.c.y, self.a.y]
        plt.plot(x, y, 'b')

class Node(object):
    def __init__(self, x, y, nr, on_el, u):
        self.x = x
        self.y = y
        self.nr = nr
        self.on_el = on_el
        self.u = u

class Mesh(object):
    '''
    classdocs
    '''
    def __init__(self, geometry, x_step, y_step):
        self.geometry=geometry
        self.x_step = x_step
        self.y_step = y_step
        self.elements=[]
        self.nodes=[]
        self.num_nodes_x = int((geometry.x_max-geometry.x_min)/x_step)+2
        self.num_nodes_y = int((geometry.y_max-geometry.y_min)/y_step)+2
        self.grid=np.zeros((self.num_nodes_x, self.num_nodes_y), dtype=np.int)
        self.grid= self.grid-1
        
    def generate_mesh(self):
        util.tic()
        node_nr = 0;
        for i in range(self.num_nodes_x):
            for j in range(self.num_nodes_y):
                x = i*self.x_step+self.geometry.x_min
                y = j*self.y_step+self.geometry.y_min
                is_el = self.geometry.is_electrode(x, y)
                if not is_el[0] or self.is_boundary(x, y):
                    node = Node(x, y, node_nr, is_el[0], is_el[1])
                    self.nodes.append(node)
                    self.grid[i,j] = node_nr
                    node_nr = node_nr + 1
                    self.make_elements(i, j)
        util.toc("Generating mesh: %.2f s")
        print("Num. of nodes: ", len(self.nodes))
        print("Num. of elements: ", len(self.elements))
    
    def make_elements(self, i, j):
        '''
        for the input node, tries to add two elements (bottom left ones)
        first checks that the positions have nodes
        then checks that at least one node is not on an electrode
        '''
        if i <= 0 or j <= 0:
            return
        
        on_el00 = self.nodes[self.grid[i,j]].on_el
        on_el10 = self.nodes[self.grid[i-1,j]].on_el
        on_el01 = self.nodes[self.grid[i,j-1]].on_el
        on_el11 = self.nodes[self.grid[i-1,j-1]].on_el
        
        if (self.grid[i,j-1] >= 0 and self.grid[i-1,j-1] >= 0 and
                not (on_el00 and on_el01 and on_el11)):
            a = self.nodes[self.grid[i, j]]
            b = self.nodes[self.grid[i-1, j-1]]
            c = self.nodes[self.grid[i, j-1]]
            self.elements.append(Element(a, b, c))
        if (self.grid[i-1,j] >= 0 and self.grid[i-1,j-1] >= 0 and
                not (on_el00 and on_el10 and on_el11)):
            a = self.nodes[self.grid[i, j]]
            b = self.nodes[self.grid[i-1, j]]
            c = self.nodes[self.grid[i-1, j-1]]
            self.elements.append(Element(a, b, c))
    
    def is_boundary(self, x, y):
        '''
        check if relevant neighbours are inside the electrode
        mesh structure:
        *-----*
        |    /|
        |  /  |
        |/    |
        *-----*
        '''
        x_min = self.geometry.x_min
        x_max = self.geometry.x_max
        y_min = self.geometry.y_min
        y_max = self.geometry.y_max
        
        xm = x - self.x_step
        xp = x + self.x_step
        ym = y - self.y_step
        yp = y + self.y_step
        
        if xm >= x_min and not self.geometry.is_electrode(xm, y)[0]:
            return True
        if xp <= x_max and not self.geometry.is_electrode(xp, y)[0]:
            return True
        if ym >= y_min and not self.geometry.is_electrode(x, ym)[0]:
            return True
        if yp <= y_max and not self.geometry.is_electrode(x, yp)[0]:
            return True
        if xp <= x_max and yp <= y_max and not self.geometry.is_electrode(xp, yp)[0]:
            return True
        if xm >= x_min and ym >= y_min and not self.geometry.is_electrode(xm, ym)[0]:
            return True
        return False
    
    def draw(self, nodes_or_mesh):
        util.tic()
        if nodes_or_mesh:
            x=[]
            y=[]
            for node in self.nodes:
                x.append(node.x)
                y.append(node.y)
            plt.scatter(x, y, 3, zorder=2)
        else:
            for el in self.elements:
                el.draw()
        util.toc("Drawing mesh: %.2f s")
        