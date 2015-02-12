#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import math

class UIManagerExample:
      
    def __init__(self):
        # Create the toplevel window
        window = gtk.Window()
        window.connect('destroy', lambda w: gtk.main_quit())
        window.set_size_request(800,600)
        vbox = gtk.VBox()
        window.add(vbox)

        # Create a UIManager instance
        uimanager = gtk.UIManager()

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        window.add_accel_group(accelgroup)

        # Create an ActionGroup
        actiongroup = gtk.ActionGroup('UIManagerExample')
        self.actiongroup = actiongroup

        # Create actions
        actiongroup.add_actions([('Quit', gtk.STOCK_QUIT, '_Quit me!', None,
                                  'Quit the Program', self.quit_cb),
                                 ('File', None, '_File'),
                                 ('New' , gtk.STOCK_NEW, '_New'),
                                 ('Open', gtk.STOCK_OPEN, '_Open'),
                                 ('Export', gtk.STOCK_SAVE, '_Export'),
                                 ('Settings', gtk.STOCK_EXECUTE, '_Settings'),
                                 ('Help' , None, '_Help'),
                                 ('Up' , gtk.STOCK_GO_UP, '_Up'),
                                 ('Down' , gtk.STOCK_GO_DOWN, '_Down'),
                                 ('Right' , gtk.STOCK_GO_FORWARD, '_Right'),
                                 ('Left' , gtk.STOCK_GO_BACK, '_Left'),
                                 ('About', gtk.STOCK_HELP, '_About')])
        actiongroup.get_action('Quit').set_property('short-label', '_Quit')

        # Add the actiongroup to the uimanager
        uimanager.insert_action_group(actiongroup, 0)

        # Add a UI description
        uimanager.add_ui_from_file("ui.xml")

        # Create a MenuBar
        menubar = uimanager.get_widget('/MenuBar')
        vbox.pack_start(menubar, False)

        # Create a Toolbar
        toolbar = uimanager.get_widget('/Toolbar')
        vbox.pack_start(toolbar, False)

        # Create and pack two Labels
        drawingarea = gtk.DrawingArea()
        self.drawingarea = drawingarea
        drawingarea.connect("expose-event", self.expose)
        vbox.pack_start(drawingarea)

        window.show_all()
        return

    def expose(self, widget, event):

        cr = widget.window.cairo_create()

        cr.set_line_width(9)
        cr.set_source_rgb(0.7, 0.2, 0.0)
                
        w = widget.allocation.width
        h = widget.allocation.height

        cr.translate(w/2, h/2)
        cr.arc(0, 0, 50, 0, 2*math.pi)
        cr.stroke_preserve()
        
        cr.set_source_rgb(0.3, 0.4, 0.6)
        cr.fill()

    def quit_cb(self, b):
        print 'Quitting program'
        gtk.main_quit()

if __name__ == '__main__':
    UIManagerExample()
    gtk.main()
