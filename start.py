#!/usr/bin/env python2.7

import gtk

def button_clicked(button):
    print "Hello world"

def main():
    window = gtk.Window()
    window.set_default_size(240, 100)
    window.set_title("Hello world app")
    window.connect('destroy', lambda w: gtk.main_quit())
    
    button = gtk.Button("Press me")
    button.connect('clicked',button_clicked)
    button.show()

    window.add(button)
    window.present()
    
    gtk.main()

if __name__ == '__main__':
    main()
