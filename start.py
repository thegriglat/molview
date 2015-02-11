#!/usr/bin/env python2.7

import sys
try:
    import gtk
except:
    print "Cannot import gtk. Please be sure that your PYTHONPATH is set correctly"
    sys.exit(1)

def button_clicked(button):
    print "Hello world"

class MainWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.button = gtk.Button(label="Click here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print "Hello world!"

def main():
    window = MainWindow()
    window.set_default_size(240, 100)
    window.set_title("Hello world app")
    window.connect('destroy', lambda w: gtk.main_quit())
    
    window.show_all()
    window.present()
    
    gtk.main()

if __name__ == '__main__':
    main()
