#!/usr/bin/env python

import math
from data import *

class Structure:
    def __init__(self):
        self.atoms = []
        self.bonds = []
    def to2D(self, phi = 0):
        return [a.to2D(phi) for a in self.atoms]
            
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
    def to2D(self, phi = 0):
        xphi = self.xyz[0] * math.cos(phi)
        yphi = self.xyz[1] 
        zphi = self.xyz[2] * math.cos(math.pi/2 - phi)
        #return ((xphi, yphi, zphi), self.radius)
        return ((xphi, zphi), self.radius)

def matMul(a, b):
    zip_b = zip(*b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_b] for row_a in a]