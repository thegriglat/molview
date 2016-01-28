#!/usr/bin/env python

import json

class Settings:
    DEFAULTFILE = "settings.cfg"
    filename = ""
    settings = {}
    def __init__(self, filename):
        self.filename = filename
        self.parseConfigFile(filename)
    
    def parseConfigFile(self, filename):
      with open(filename, 'r') as f:
        self.settings = json.load(f)

    def saveConfigFile(self, filename):
      with open(filename, 'w') as f:
        json.dump(f, self.settings)
