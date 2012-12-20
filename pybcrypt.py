#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""PyGTK wrapper of bcrypt"""

import sys
import pygtk
pygtk.require('2.0')
import gtk
import pango
import subprocess

class PyBcrypt:

    def delete_event(self, widget, event, data=None):
        """docstring for delete_event"""
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        """docstring for destroy"""
        gtk.main_quit()

    def choice(self, widget, data=None):
        """docstring for choice"""
        self.fcdiabtn1 = gtk.Button("Choice")
        self.fcdiabtn2 = gtk.Button("Cancel")
        self.fcdia = gtk.FileChooserDialog("Choice File", action = gtk.FILE_CHOOSER_ACTION_OPEN, buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        #self.fcdia.show()
        res = self.fcdia.run()
        if res == gtk.RESPONSE_CANCEL:
            self.fcdia.destroy()
        if res == gtk.RESPONSE_OK:
            self.ofile.set_text(self.fcdia.get_filename())
            self.fcdia.destroy()
            filename = self.ofile.get_text()
            if filename[-4:len(filename)] == ".bfe":
                self.pswd2.set_sensitive(False)
            else:
                self.pswd2.set_sensitive(True)

    def on_ofile_change(self, widget, event=None):
        """docstring for on_change"""
        filename = self.ofile.get_text()
        if filename[-4:len(filename)] == ".bfe":
            self.pswd2.set_sensitive(False)
        else:
            self.pswd2.set_sensitive(True)

    def bcrypt(self, widget, data=None):
        """docstring for bcrypt"""
        #print "bcrypt something"
        password = self.pswd1.get_text()
        if len(password) < 8:
            attr = pango.AttrList()
            attr.insert(pango.AttrForeground(65535, 0, 0, 0, -1))
            self.label.set_text("Pswd at least 8 char!")
            self.label.set_attributes(attr)
            return
        openfile = self.ofile.get_text()
        if openfile[-4:len(openfile)] == ".bfe":
            tempf = file('/tmp/temppybcrypt', 'w')
            tempf.write(password + "\n")
            tempf.close()
            tempf = file('/tmp/temppybcrypt', 'r')
            subprocess.call(["bcrypt", openfile], stdin = tempf)
            tempf.close()
            subprocess.call(["rm", "-f", "/tmp/temppybcrypt"])
            gtk.main_quit()
        else:
            pswd2 = self.pswd2.get_text()
            if password != pswd2:
                attr = pango.AttrList()
                attr.insert(pango.AttrForeground(65535, 0, 0, 0, -1))
                self.label.set_text("Password not equal!")
                self.label.set_attributes(attr)
            else:
                # TODO 去掉临时密码文件
                tempf = file('/tmp/temppybcrypt', 'w')
                tempf.write(password + "\n")
                tempf.write(password + "\n")
                tempf.close()
                tempf = file('/tmp/temppybcrypt')
                #subprocess.call(["echo", "-e", echopassword, "|", "bcrypt", "/home/keepzero/testfile"])
                subprocess.call(["bcrypt", openfile], stdin = tempf)
                tempf.close()
                subprocess.call(["rm", "-f", "/tmp/temppybcrypt"])
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
