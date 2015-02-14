#!/usr/bin/env python

from math import *
from data import *

class Structure:
    def __init__(self):
        self.atoms = []
        self.bonds = []
    def to2D(self, phi = 0, psi = 0):
        return [a.to2D(phi, psi) for a in self.atoms]
            
    def read_from_file(self, filename, filetype = "xyz"):
        if filetype == "xyz":
            f = open(filename)
            for l in f.readlines():
                l = l.strip()
                (label, x, y, z) = l.split()
                a = Atom()
                a.xyz = [float(x), float(y), float(z)]
                a.label = label
                a.radius = data["atoms"]["radius"][label]
                self.atoms.append(a)
                del a

class Atom:
    def __init__(self):
        self.xyz = [0.0, 0.0, 0.0]
        self.label = ""
        self.radius = 1.0
    def to2D(self, phi = 0, psi = 0):
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
        xnew = xyz_new[0][0]
        ynew = xyz_new[1][0]
        #return ((xphi, yphi, zphi), self.radius)
        return ((xnew, ynew), self.radius)

def matMul(a, b):
    zip_b = zip(*b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_b] for row_a in a]