#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import math
from structure import *


class MolViewUI:
    x, y = 0, 0      
    xoy = 0
    xoz = 0
    scaleFactor = 20.0

    def __init__(self):
        # Create the toplevel window
        window = gtk.Window()
        self.window = window
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
                                 ('Export', gtk.STOCK_SAVE, '_Save as PNG'),
                                 ('Settings', gtk.STOCK_EXECUTE, '_Settings'),
                                 ('Help' , None, '_Help'),
                                 ('Up' , gtk.STOCK_GO_UP, '_Up'),
                                 ('Down' , gtk.STOCK_GO_DOWN, '_Down'),
                                 ('Right' , gtk.STOCK_GO_FORWARD, '_Right'),
                                 ('Left' , gtk.STOCK_GO_BACK, '_Left'),
                                 ('Centralize' , gtk.STOCK_REFRESH, '_Centralize'),
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

        scale = gtk.HScale(gtk.Adjustment(value = 1,
                                           lower = 0.1,
                                           upper = 101,
                                           step_incr = 0.1,
                                           page_incr = 0.1,
                                           page_size = 1))
            
        self.scale = scale
        scale.set_value(self.scaleFactor)
        scale.connect('value-changed', self.scaleStructure, None, self.scaleFactor)
        vbox.pack_start(scale, False, False)
        vbox.pack_start(drawingarea)
        
        # Move buttons
        upbutton = uimanager.get_widget("/Toolbar/Up")
        downbutton = uimanager.get_widget("/Toolbar/Down")
        rightbutton = uimanager.get_widget("/Toolbar/Right")
        leftbutton = uimanager.get_widget("/Toolbar/Left")
        upbutton.connect("clicked"   , self.moveImage, None, "y", -1 * math.pi / 12)
        downbutton.connect("clicked" , self.moveImage, None, "y", +1 * math.pi / 12)
        rightbutton.connect("clicked", self.moveImage, None, "x", +1 * math.pi / 12)
        leftbutton.connect("clicked" , self.moveImage, None, "x", -1 * math.pi / 12)
        
        # Menu buttons
        newbutton = uimanager.get_widget("/Toolbar/New")
        newbutton.connect("clicked", self.cleanStructure, None)
        menunewbutton = uimanager.get_widget("/MenuBar/File/New")
        menunewbutton.connect("activate", self.cleanStructure, None)
        openbutton = uimanager.get_widget("/Toolbar/Open")
        menuopenbutton = uimanager.get_widget("/MenuBar/File/Open")
        openbutton.connect('clicked', self.openFileDialog, None)
        menuopenbutton.connect("activate", self.openFileDialog, None)
        exportbutton = uimanager.get_widget("/MenuBar/File/Export")
        exportbutton.connect("activate", self.saveFileDialog, None)
        helpbutton = uimanager.get_widget("/MenuBar/Help/About")
        helpbutton.connect("activate", self.aboutWindow, None)
        centralizebutton = uimanager.get_widget("/Toolbar/Centralize")
        centralizebutton.connect("clicked", self.centralize, None)

        window.show_all()
        return

    def centralize(self, windget, event):
        s.centralize()
        self.drawingarea.queue_draw()

    def saveFileDialog(self, widget, event):
        def exportAsPNG(drawable, filename):
            colormap = drawable.get_colormap()
            pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, 0, 8, *drawable.get_size())
            pixbuf = pixbuf.get_from_drawable(drawable, colormap, 0,0,0,0, *drawable.get_size())
            pixbuf.save(filename, 'png')

        dialog = gtk.FileChooserDialog("Save file in png format ...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("PNG files")
        filter.add_pattern("*.png")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            exportAsPNG(self.drawingarea.window, dialog.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            print 'No file saved'
        dialog.destroy()
        return True

    def openFileDialog(self, widget, event):
        dialog = gtk.FileChooserDialog("Open file ...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("XYZ files")
        filter.add_pattern("*.xyz")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            s.read_from_file(dialog.get_filename())
            self.drawingarea.queue_draw()
        elif response == gtk.RESPONSE_CANCEL:
            print 'No files selected'
        dialog.destroy()
        if Settings.settings['app']['autocentralize']:
            s.centralize()
        if Settings.settings['app']['autoscale']:
          linewidth = s.getLinearSize()
          initscale = max(self.window.get_size()) / linewidth / 4.0
          self.scale.set_value(initscale)

        return True

    def cleanStructure(self, widget, event):
        global s
        s = Structure()
        self.drawingarea.queue_draw()

    def moveImage(self, widget, event, dim, delta):
        if dim == "y":
            self.xoy += delta
        elif dim == "x":
            self.xoz += delta
        self.drawingarea.queue_draw()

    def expose(self, widget, event):
        width  = widget.allocation.width
        height = widget.allocation.height
        for (label, coord, radius) in s.to2D(self.xoy, self.xoz, self.scaleFactor):
            cr = widget.window.cairo_create()
            cr.translate(width / 2 ,height / 2)
            cr.arc(coord[0], coord[1], radius, 0, 2 * math.pi)
            cr.set_source_rgb(Settings.settings["atoms"][label]["color"]["red"],
                              Settings.settings["atoms"][label]["color"]["green"],
                              Settings.settings["atoms"][label]["color"]["blue"]
                             )
            cr.stroke_preserve()
            cr.fill()
                
    def quit_cb(self, b):
        gtk.main_quit()

    def doRotate(self, widget, x, y):
        dx, dy = 0, 0
        if x != self.x:
            dx = x - self.x
        if y != self.y:
            dy = y - self.y
        self.xoy += dy * math.pi / 180
        self.xoz += dx * math.pi / 180
        self.x = x
        self.y = y
        widget.queue_draw()
        

    def rotateCamera(self, widget, event):
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
        if state & gtk.gdk.BUTTON1_MASK:
            self.doRotate(widget, x, y)

    def aboutWindow(self, widget, event):
      window = gtk.Window()
      window.set_size_request(350,100)
      label = gtk.Label("This program has GPLv3 license.\nSource code is hosted on\nhttps://github.com/thegriglat/molview")
      window.add(label)
      window.show_all()

    def scaleStructure(self, widget, event, scale):
      if widget.get_value() > 0.9 * widget.get_adjustment().get_upper():
          adj = widget.get_adjustment()
          adj.set_upper(adj.get_upper() + 1)
          widget.set_adjustment(adj)
          del adj
      elif widget.get_value() < 0.1 * widget.get_adjustment().get_upper():
          adj = widget.get_adjustment()
          if adj.get_upper() - 1 > 0:
            adj.set_upper(adj.get_upper() - 1 )
          widget.set_adjustment(adj)
          del adj

      self.scaleFactor = float(widget.get_value())
      self.drawingarea.queue_draw()


Settings = Settings("settings.cfg")

if __name__ == '__main__':
    MolViewUI = MolViewUI()
    s = Structure()
    gtk.main()
