import wx
import os

from ui_auth import AuthFrame
from db_func import DBInteraction


if __name__ == '__main__':
    db = DBInteraction()

    if not os.path.exists("users.db"):
        db.db_init()

    app = wx.App()
    frame = AuthFrame(parent=None)
    frame.Show()

    app.MainLoop()
