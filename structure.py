#!/usr/bin/env python

from math import *
from settings import *
import main

class Structure:
    def __init__(self):
        self.atoms = []
        self.bonds = []
    def to2D(self, phi = 0, psi = 0, scale = 1.0):
        # sort by Z axis
        return sorted([a.to2D(phi, psi, scale) for a in self.atoms], key = lambda test: test[1][2])
        
    def read_from_file(self, filename, filetype = "xyz"):
        self.__init__()
        if filetype == "xyz":
            f = open(filename)
            for l in f.readlines():
                l = l.strip()
                (label, x, y, z) = l.split()
                a = Atom()
                a.xyz = [float(x), float(y), float(z)]
                a.label = label
                a.radius = main.Settings.settings["atoms"][label]["radius"]
                self.atoms.append(a)
                del a

class Atom:
    def __init__(self):
        self.xyz = [0.0, 0.0, 0.0]
        self.label = ""
        self.radius = 1.0

    def getRadius(self, scale = 1.0):
        return self.radius * scale
    
    def to2D(self, phi = 0, psi = 0, scale = 1.0):
        oldxyz = [[self.xyz[0]], [self.xyz[1]], [self.xyz[2]]]
        rotate1 = [
            [1,           0,        0],
            [0,    cos(phi), sin(phi)],
            [0, -1*sin(phi), cos(phi)]
                  ]
        rotate2 = [
            [cos(psi), 0, -1*sin(psi)],
            [       0, 1,           0],
            [sin(psi), 0,    cos(psi)]
                  ]
        xyz_new = matMul(matMul(rotate1, rotate2), oldxyz)
        return (self.label, (scale * xyz_new[0][0], scale * xyz_new[1][0], scale * xyz_new[2][0]), self.getRadius(scale))

def matMul(a, b):
    zip_b = zip(*b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_b] for row_a in a]
