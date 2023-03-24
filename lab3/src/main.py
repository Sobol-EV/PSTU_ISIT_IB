import wx

from ui import MainFrame

if __name__ == '__main__':

    app = wx.App()
    frame = MainFrame(parent=None)
    frame.Show()

    app.MainLoop()
