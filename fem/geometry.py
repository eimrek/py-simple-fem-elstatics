'''
Created on 11 Jan 2015

@author: Kristjan
'''
import matplotlib.patches as pth
import matplotlib.pyplot as plt

class CircularElectrode(object):
    
    def __init__(self, x, y, r, u):
        self.x=x
        self.y=y
        self.r=r
        self.u=u
    
    def is_inside(self, x, y):
        if (self.x-x)**2 + (self.y-y)**2 <= self.r**2:
            return True
        return False
    
    def image(self):
        return pth.Circle((self.x,self.y),self.r,color='0.75', zorder=1)

class RectangularElectrode(object):
    '''
    Rotation?
    '''
    def __init__(self, x1, y1, x2, y2, u):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.u=u
    
    def is_inside(self, x, y):
        x_inside = x <= self.x1 and x >= self.x2 or x >= self.x1 and x <= self.x2
        y_inside = y <= self.y1 and y >= self.y2 or y >= self.y1 and y <= self.y2
        if x_inside and y_inside:
            return True
        return False
    
    def is_inside2(self, x, y):
        '''
        Check based on inner products
        '''
        amab = self.y2*(y-self.y1)
        abab = self.y2**2
        amad = self.x2*(x-self.x1)
        adad = self.x2**2
        if 0 <= amab and amab <= abab  and 0 <= amad and amad <= adad:
            return True
        return False
    
    def image(self):
        w = self.x2-self.x1
        h = self.y2-self.y1
        return pth.Rectangle((self.x1, self.y1), w, h, angle=0.0, color='0.75', zorder=1)

class Geometry(object):
    '''
    classdocs
    '''

    def __init__(self, x_min=-100, x_max=100, y_min=-100, y_max=100):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.electrodes=[]
    
    def add_circular(self, x, y, r, u):
        self.electrodes.append(CircularElectrode(x, y, r, u))
        
    def add_rectangular(self, x1, y1, x2, y2, u):
        self.electrodes.append(RectangularElectrode(x1, y1, x2, y2, u))
    
    def is_electrode(self, x, y):
        for el in self.electrodes:
            if el.is_inside(x, y):
                return [True, el.u]
        return [False, 0]
    
    def draw(self):
        axes = plt.gca()
        for el in self.electrodes:
            axes.add_patch(el.image())
        axes.set_xlim([self.x_min, self.x_max])
        axes.set_ylim([self.y_min, self.y_max])
    
    