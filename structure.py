#!/usr/bin/env python

import math

class Structure:
    def __init__(self):
        self.atoms = []
        self.bonds = []
    def to2D(self, phi = 0):
        return [a.to2D(phi) for a in self.atoms]
            

class Atom:
    def __init__(self):
        self.xyz = [0.0, 0.0, 0.0]
        self.label = ""
        self.radius = 1.0
    def to2D(self, phi = 0):
        xphi = self.xyz[0] * math.cos(phi)
        yphi = self.xyz[1] 
        zphi = self.xyz[2] * math.cos(math.pi/2 - phi)
        return ((xphi, yphi, zphi), self.radius)
