# -*- coding: utf-8 -*-
"""
Created on Mon May 19 12:48:35 2014

@author: teo
"""

import wx, os

class MyApp(wx.App):
    def OnInit(self):
        screenSize = wx.GetDisplaySize()
        appHeight = 500
        appWidth = 800
        xpos = (screenSize[0] - appWidth)/2
        ypos = (screenSize[1] - appHeight)/2
        
        if xpos < 0:
            xpos = 0
        else:
            pass
        if ypos < 0:
            ypos = 0
        else:
            pass
        
        frame = MyFrame("BeaT Project", (xpos, ypos), (appWidth, appHeight))
        frame.Show()
        self.SetTopWindow(frame)
        return True

class MyFrame(wx.Frame):
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        
        menuFile = wx.Menu()
        menuFile.Append(1, "O&pen...")
        menuFile.AppendSeparator()
        menuFile.Append(2, "E&xit")
        
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to BeaT!")
        self.Bind(wx.EVT_MENU, self.OnOpen, id=1)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=2)
    def OnQuit(self, event):
        self.Close()
    def OnOpen(self,e):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
    
    def OnAbout(self, event):
        wx.MessageBox("This is a wxPython BeaT sample","About BeaT",
                      wx.OK | wx.ICON_INFORMATION, self)

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()