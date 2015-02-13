#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from structure import *

class MolViewUI:
    x, y = 0, 0      
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
        actiongroup = gtk.ActionGroup('MolViewUI')
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

        drawingarea = gtk.DrawingArea()
        self.drawingarea = drawingarea
        drawingarea.connect("expose-event", self.expose)
        drawingarea.connect("motion_notify_event", self.rotateCamera)
        drawingarea.set_events(gtk.gdk.EXPOSURE_MASK
                            | gtk.gdk.LEAVE_NOTIFY_MASK
                            | gtk.gdk.BUTTON_PRESS_MASK
                            | gtk.gdk.POINTER_MOTION_MASK
                            | gtk.gdk.POINTER_MOTION_HINT_MASK)
        drawingarea.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        vbox.pack_start(drawingarea)
        
        # Move buttons        
        upbutton = uimanager.get_widget("/Toolbar/Up")
        downbutton = uimanager.get_widget("/Toolbar/Down")
        rightbutton = uimanager.get_widget("/Toolbar/Right")
        leftbutton = uimanager.get_widget("/Toolbar/Left")
        upbutton.connect("clicked"   , self.moveImage, None, "y", -10)
        downbutton.connect("clicked" , self.moveImage, None, "y", +10)
        rightbutton.connect("clicked", self.moveImage, None, "x", +10)
        leftbutton.connect("clicked" , self.moveImage, None, "x", -10)
        window.show_all()
        return

    def moveImage(self, widget, event, dim, delta):
        if dim == "y":
            self.y += delta
        elif dim == "x":
            self.x += delta
        return True

    def repaint(self, widget):
        widget.queue_clear()
        cr = widget.window.cairo_create()
        self.cr = cr
        cr.set_line_width(9)
        cr.set_source_rgb(0.7, 0.2, 0.0)
                
        self.width  = widget.allocation.width
        self.height = widget.allocation.height

        cr.translate(self.x ,self.y)
        cr.arc(0, 0, 50, 0, 2*math.pi)
        cr.stroke_preserve()
        
        cr.set_source_rgb(0.3, 0.4, 0.6)
        cr.fill()

    def expose(self, widget, event):
        self.repaint(widget)

    def quit_cb(self, b):
        print 'Quitting program'
        gtk.main_quit()

    def move_arc(self, widget, x, y):
        self.x = x
        self.y = y
        self.repaint(widget)
        return True
        

    def rotateCamera(self, widget, event):
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
        if state & gtk.gdk.BUTTON1_MASK:
            self.move_arc(widget, x, y)
        return True


if __name__ == '__main__':
    MolViewUI()
    gtk.main()
