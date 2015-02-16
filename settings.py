#!/usr/bin/env python

import yaml

class Settings:
    DEFAULTFILE = "settings.yaml"
    filename = ""
    settings = {}

    def __init__(self, filename):
        self.filename = filename
        self.parseConfigFile(filename)
    
    def parseConfigFile(self, filename):
        try:
            self.settings  = yaml.load(open(filename, 'r'))
        except:
            print "Cannot load settings"

    def saveConfigFile(self, filename):
        f = open(filename, 'w')
        f.write(yaml.dump(self.settings))
        f.close()
