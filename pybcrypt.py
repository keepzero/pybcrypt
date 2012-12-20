#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""PyGTK wrapper of bcrypt"""

import sys
import pygtk
pygtk.require('2.0')
import gtk
import pango
import subprocess
from subprocess import Popen, PIPE

class PyBcrypt:

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        """Quit PyGTK"""
        gtk.main_quit()

    def choice(self, widget, data=None):
        """Choice file with FileChooserDialog"""
        self.fcdia = gtk.FileChooserDialog("Choice File", \
                action = gtk.FILE_CHOOSER_ACTION_OPEN, \
                buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        response = self.fcdia.run()
        if response == gtk.RESPONSE_CANCEL:
            self.fcdia.destroy()
        if response == gtk.RESPONSE_OK:
            self.ofile.set_text(self.fcdia.get_filename())
            self.fcdia.destroy()
            self.change_pswd_sen()

    def change_pswd_sen(self):
        """Set the pswd2 sensitive"""
        filename = self.ofile.get_text()
        if filename[-4:len(filename)] == ".bfe":
            self.pswd2.set_sensitive(False)
        else:
            self.pswd2.set_sensitive(True)

    def on_ofile_change(self, widget, event=None):
        """When ofile entry change"""
        self.change_pswd_sen()

    def pswd_prompt(self, prompt = "Input password:"):
        """Prompt password info"""
        attr = pango.AttrList()
        attr.insert(pango.AttrForeground(65535, 0, 0, 0, -1))
        self.label.set_text(prompt)
        self.label.set_attributes(attr)

    def bcrypt(self, widget, data=None):
        """Encrypt or decrypt a file"""
        #print "bcrypt something"
        password = self.pswd1.get_text()
        if len(password) < 8:
            self.pswd_prompt("Pswd at least 8 chars!")
            return False

        filename = self.ofile.get_text()
        if filename[-4:len(filename)] == ".bfe":
            po = Popen(('bcrypt', filename), stdin = PIPE, stdout = PIPE)
            result = po.communicate(password + "\n")
            print result[0]

            gtk.main_quit()
        else:
            pswd2 = self.pswd2.get_text()
            if password != pswd2:
                self.pswd_prompt("Password not equal!")
            else:
                po = Popen(('bcrypt', filename), stdin = PIPE, stdout = PIPE)
                result = po.communicate(password + "\n" + password + "\n")
                print result[0]
                gtk.main_quit()

    def __init__(self):
        """docstring for __init__"""
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("PyBcrypt")
        self.window.set_size_request(280, 180)
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        self.vbox = gtk.VBox(False, 5)
        self.hbox = gtk.HBox(True, 3)

        self.ochoice = gtk.Button("Choise file")
        self.ofile = gtk.Entry()
        self.ofile.add_events(gtk.gdk.KEY_RELEASE_MASK)
        self.ofile.connect("key-release-event", self.on_ofile_change)
        self.label = gtk.Label("Input Password:")
        self.pswd1 = gtk.Entry()
        self.pswd1.set_visibility(False)
        self.pswd2 = gtk.Entry()
        self.pswd2.set_visibility(False)
        #self.pswd2.set_sensitive(False)
        self.vbox.add(self.ochoice)
        self.vbox.add(self.ofile)
        self.vbox.add(self.label)
        self.vbox.add(self.pswd1)
        self.vbox.add(self.pswd2)

        ## FileChooserDialog
        self.ochoice.connect("clicked", self.choice, None)

        self.valign = gtk.Alignment(0, 1, 0 ,0)
        self.vbox.pack_start(self.valign)
        
        self.ok = gtk.Button("OK")
        self.ok.set_size_request(70, 30)
        self.ok.connect("clicked", self.bcrypt, None)
        self.close = gtk.Button("Close")
        self.close.connect_object("clicked", gtk.Widget.destroy, self.window)

        self.hbox.add(self.ok)
        self.hbox.add(self.close)

        self.halign = gtk.Alignment(1, 0, 0, 0)
        self.halign.add(self.hbox)

        self.vbox.pack_start(self.halign, False, False, 3)

        self.window.add(self.vbox)

        # init args
        if len(sys.argv) == 2:
            self.ofile.set_text(sys.argv[1])
            filename = self.ofile.get_text()
            if filename[-4:len(filename)] == ".bfe":
                self.pswd2.set_sensitive(False)
            else:
                self.pswd2.set_sensitive(True)

        self.window.show_all()
    
    def main(self):
        gtk.main()

if __name__ == '__main__':
    pb = PyBcrypt()
    pb.main()
