'''
Created on 18 Jan 2015

@author: Kristjan
'''
import numpy as np
import fem.util as util
import matplotlib.pyplot as plt

class Setup(object):
    '''
    Sets up the matrix equation based on the mesh and geometry
    '''
    
    def __init__(self, mesh):
        self.mesh = mesh
        
    def element_mat(self, elem):
        '''
        Equations from book p. 104
        '''
        beta = 1 #electric permittivity ?
        bi = elem.b.y-elem.c.y
        bj = elem.c.y-elem.a.y
        bm = elem.a.y-elem.b.y
        ci = elem.c.x-elem.b.x
        cj = elem.a.x-elem.c.x
        cm = elem.b.x-elem.a.x
        S = 0.5*(bi*cj-bj*ci)
        
        B = np.matrix([bi, bj, bm])
        C = np.matrix([ci, cj, cm])
        
        K = beta/(4*S)*(np.transpose(B)*B+np.transpose(C)*C)
        return K
    
    def element_mat_axisym(self, elem):
        '''
        Equations from book p. 160
        in our notation r=x; z=y
        '''
        beta = 1 #electric permittivity ? = epsilon from p160
        bi = elem.b.y-elem.c.y
        bj = elem.c.y-elem.a.y
        bm = elem.a.y-elem.b.y
        ci = elem.c.x-elem.b.x
        cj = elem.a.x-elem.c.x
        cm = elem.b.x-elem.a.x
        
        S = 0.5*(bi*cj-bj*ci)
        r0 = 1/3*(elem.a.x+elem.b.x+elem.c.x)
        
        B = np.matrix([bi, bj, bm])
        C = np.matrix([ci, cj, cm])
        
        K = (beta*2*np.pi)/(4*S)*r0*(np.transpose(B)*B+np.transpose(C)*C)
        return K
        
    
    def init_system_mat(self, is_axisym):
        util.tic()
        num_nodes = len(self.mesh.nodes)
        self.sys = np.zeros((num_nodes, num_nodes)) # SYSTEM MATRIX
        for el in self.mesh.elements:
            if is_axisym:
                k = self.element_mat_axisym(el)
            else:
                k = self.element_mat(el)
            for i in range(len(el.nodes)):
                for j in range(len(el.nodes)):
                    nr1 = el.nodes[i].nr
                    nr2 = el.nodes[j].nr
                    self.sys[nr1, nr2] = self.sys[nr1, nr2] + k[i,j]
        util.toc("Created the system matrix: %0.2f s")
        print("System matrix memory:", self.sys.nbytes, "bytes")
        print("Shape of the matrix:", self.sys.shape)
    
    def boundary_conditions(self):
        '''
        Incorporates the boundary conditions into the matrix equation.
        Currently uses loops, but efficient numpy matrix operations could also be used
        '''
        util.tic()
        self.b = np.zeros(len(self.mesh.nodes)) # RHS of the matrix eq
        for node in self.mesh.nodes:
            if node.on_el:
                for i in range(len(self.mesh.nodes)):
                    if not self.mesh.nodes[i].on_el:
                        # T.PLANK'S SOL DIDN'T DO THIS!
                        self.b[i] = self.b[i]-self.sys[i, node.nr]*node.u
                        #print(self.sys[i, node.nr]*node.u)
                    self.sys[i, node.nr] = 0
                    self.sys[node.nr, i] = 0
                self.b[node.nr] = node.u
                self.sys[node.nr, node.nr] = 1
        util.toc("Processed boundary conditions: %0.2f s")
        
    def solve(self, method):
        util.tic()
        if method==1:
            print("Gaussian elimination")
            self.u = self.gaussian_el(self.sys, self.b)
        else:
            print("Numpy inverse matrix")
            self.u = np.linalg.inv(self.sys).dot(self.b)
        util.toc("Solved the equation: %0.2f s")
    
    def gaussian_el(self, in_sys, in_b):
        '''
        Solves the matrix equation SYS*U=B by gaussian elimination
        Assumes that every diagonal element is non-zero
        '''
        n_rows = in_sys.shape[0]
        n_cols = in_sys.shape[1]
        sys = np.copy(in_sys)
        b = np.copy(in_b)
        eps = 1e-10
        for j in range(n_cols):
            if j%100==0:
                print("%.2f%%" % (j/n_cols*100))
            for i in range(j+1,n_rows):
                if sys[i,j] > eps or sys[i,j] < -eps:
                    k = sys[i,j]/sys[j,j]
                    for m in range(n_cols):
                        sys[i,m] = sys[i,m]-k*sys[j,m]
                    b[i] = b[i] - k*b[j]
                    
        u = np.zeros(n_rows)
        u[n_rows-1] = b[n_rows-1]/sys[n_rows-1,n_rows-1]
        for i in reversed(range(n_rows-1)):
            sum_ = 0
            for j in range(i+1,n_rows):
                sum_ += sys[i,j]*u[j]
            u[i] = (b[i]-sum_)/sys[i,i]
        return u
    
    def probe_u(self, x, y):
        a = self.mesh.geometry.is_electrode(x,y)
        if a[0]:
            return a[1]
        for el in self.mesh.elements:
            if el.in_elem(x, y):
                alp = el.lin_coef(self.u)
                return alp[0]+alp[1]*x+alp[2]*y
        return 0
    
    
    def draw_old(self):
        util.tic()
        x=[]
        y=[]
        z=[]
        for node in self.mesh.nodes:
            x.append(node.x)
            y.append(node.y)
            z.append(self.u[node.nr])
        plt.scatter(x, y, z, zorder=3)
        util.toc("Drawing solution: %.2f s")
    
    def draw(self):
        util.tic()
        x=[]
        y=[]
        z=np.zeros((self.mesh.num_nodes_x, self.mesh.num_nodes_y))
        for i in range(self.mesh.num_nodes_x):
            for j in range(self.mesh.num_nodes_y):
                if self.mesh.grid[i, j] != -1:
                    z[j,i] = self.u[self.mesh.grid[i,j]]
                else:
                    xp = i*self.mesh.x_step+self.mesh.geometry.x_min
                    yp = j*self.mesh.y_step+self.mesh.geometry.y_min
                    z[j,i] = self.mesh.geometry.is_electrode(xp,yp)[1]
        for i in range(self.mesh.num_nodes_x):
            xp = i*self.mesh.x_step+self.mesh.geometry.x_min
            x.append(xp)
        for j in range(self.mesh.num_nodes_y):
            yp = j*self.mesh.y_step+self.mesh.geometry.y_min
            y.append(yp)
        plt.contourf(x, y, z, 30, zorder=0)
        plt.colorbar()
        util.toc("Drawing solution: %.2f s")
        