import wx
import wx.xrc
import wx.richtext
import wx.dataview

import re
import collections
import hashlib

from db_func import DBInteraction
import text_values_elements as tve


class AuthFrame(wx.Frame):
    CODE_AUTH = 100

    def __init__(
            self, parent, title=tve.NAME_WINDOW_AUTH,
            size=(500, 200), pos=wx.DefaultPosition
    ):
        super().__init__(
            parent, title=title, size=size, pos=pos
        )
        self.db = DBInteraction()
        self.count_error = 3
        self.response = None
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(14)
        panel.SetFont(font)

        h_box_login = wx.BoxSizer(wx.HORIZONTAL)
        text_login = wx.StaticText(panel, label=tve.TEXT_LOGIN_AUTH)
        self.field_login = wx.TextCtrl(panel)
        h_box_login.Add(text_login, flag=wx.RIGHT, border=41)
        h_box_login.Add(self.field_login, proportion=1)
        vbox.Add(
            h_box_login,
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
            border=10
        )

        h_box_pwd = wx.BoxSizer(wx.HORIZONTAL)
        text_pwd = wx.StaticText(panel, label=tve.TEXT_PASSWORD_AUTH)
        self.field_pwd = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        h_box_pwd.Add(text_pwd, flag=wx.RIGHT, border=8)
        h_box_pwd.Add(self.field_pwd, proportion=1)
        vbox.Add(
            h_box_pwd,
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
            border=10
        )

        text_empty = wx.StaticText(panel)
        btn_login = wx.Button(
            panel, id=self.CODE_AUTH, label=tve.BUTTON_AUTH, size=(300, 40)
        )
        h_box_button_login = wx.BoxSizer(wx.HORIZONTAL)
        h_box_button_login.Add(text_empty, flag=wx.RIGHT, border=102)
        h_box_button_login.Add(btn_login, proportion=1)

        vbox.Add(
            h_box_button_login,
            flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=10
        )

        panel.SetSizer(vbox)

        self.Centre(wx.BOTH)

        btn_login.Bind(wx.EVT_BUTTON, self.Authorization, id=self.CODE_AUTH)

        self.field_login.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.field_pwd.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)

        self.field_login.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
        self.field_pwd.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)

    @staticmethod
    def hash_in_md5(pwd):
        return hashlib.md5(pwd.encode('utf-8')).hexdigest()

    def Authorization(self, event):
        login = self.field_login.GetLineText(0)
        pwd = self.field_pwd.GetLineText(0)
        if pwd:
            pwd_hash = self.hash_in_md5(pwd)
        else:
            pwd_hash = None
        self.response = self.db.get_user(login)
        if self.response:
            self.response = self.response[0]
            if (self.response['login'] == login) and \
                    (self.response["password_hash"] == pwd_hash):
                self.count_error = 3
                if not self.response['is_block']:
                    if self.response['is_new']:
                        self.OpenNewPwdWindow(self.response, self.db)
                    else:
                        self.OpenPersonalAreaWindow(
                            self.response, self.db
                        )
                else:
                    self.msgBan()
            else:
                self.failedAuth()
        else:
            self.failedAuth()

    @staticmethod
    def msgBan():
        return wx.MessageBox(
            tve.MSG_BLOCK_USER,
            tve.NAME_WINDOW_ERROR_BAN, wx.OK | wx.OK_DEFAULT
        )

    def failedAuth(self):
        self.count_error -= 1
        if self.count_error <= 0:
            self.Close()
            exit(1)
        return wx.MessageBox(
            tve.error_auth(self.count_error),
            tve.NAME_WINDOW_ERROR_AUTH, wx.OK | wx.OK_DEFAULT
        )

    def onSetFocus(self, event):
        event.GetEventObject().SetBackgroundColour("#b2dfdb")
        event.Skip()

    def onKillFocus(self, event):
        event.GetEventObject().SetBackgroundColour("#FFF")
        event.Skip()

    def OpenNewPwdWindow(self, response, db: DBInteraction):
        frame = UpdatePasswordFrame(response, db)
        self.Close()

    def OpenPersonalAreaWindow(self, response, db: DBInteraction):
        frame = PersonalAreaFrame(response, db)
        self.Close()


class UpdatePasswordFrame(AuthFrame):
    CODE_BUTTON_CONFIRM = 200

    def __init__(self, response, db: DBInteraction):
        wx.Frame.__init__(
            self, parent=None, id=wx.ID_ANY, title=tve.NAME_WINDOW_UPDATE_PASSWORD, pos=wx.DefaultPosition,
            size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
        )

        self.Show()
        self.response = response
        self.db = db

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizerMain = wx.BoxSizer(wx.VERTICAL)
        bSizerOldPwd = wx.BoxSizer(wx.VERTICAL)

        self.TextOldPwd = wx.StaticText(
            self, wx.ID_ANY, tve.TEXT_OLD_PASSWORD,
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.TextOldPwd.Wrap(-1)
        self.TextOldPwd.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerOldPwd.Add(self.TextOldPwd, 0, wx.ALL | wx.EXPAND, 3)

        self.fieldOldPwd = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
            wx.DefaultSize, wx.TE_PASSWORD
        )
        bSizerOldPwd.Add(self.fieldOldPwd, 0, wx.ALL | wx.EXPAND, 5)

        bSizerMain.Add(bSizerOldPwd, 0, wx.EXPAND, 5)

        bSizerNewPwd = wx.BoxSizer(wx.VERTICAL)

        self.TextNewPwd = wx.StaticText(
            self, wx.ID_ANY, tve.TEXT_NEW_PASSWORD,
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.TextNewPwd.Wrap(-1)
        self.TextNewPwd.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerNewPwd.Add(self.TextNewPwd, 0, wx.ALL, 3)

        self.fieldNewPwd = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
            wx.DefaultSize, wx.TE_PASSWORD
        )
        bSizerNewPwd.Add(self.fieldNewPwd, 0, wx.ALL | wx.EXPAND, 5)

        bSizerMain.Add(bSizerNewPwd, 0, wx.EXPAND, 5)

        bSizerConfirmPwd = wx.BoxSizer(wx.VERTICAL)

        self.TextConfirmPwd = wx.StaticText(
            self, wx.ID_ANY, tve.TEXT_CONFIRM_NEW_PASSWORD,
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.TextConfirmPwd.Wrap(-1)
        self.TextConfirmPwd.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerConfirmPwd.Add(self.TextConfirmPwd, 0, wx.ALL, 3)

        self.fieldConfirmPwd = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0
        )
        bSizerConfirmPwd.Add(self.fieldConfirmPwd, 0, wx.ALL | wx.EXPAND, 3)

        bSizerMain.Add(bSizerConfirmPwd, 0, wx.EXPAND, 5)

        bSizerRulesAndButton = wx.BoxSizer(wx.VERTICAL)

        self.TextRulesPwd = wx.richtext.RichTextCtrl(
            self, wx.ID_ANY, self.GetTextRules(), wx.DefaultPosition, wx.DefaultSize,
            0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS
        )
        bSizerRulesAndButton.Add(self.TextRulesPwd, 1, wx.EXPAND | wx.ALL, 5)

        self.buttonConfirm = wx.Button(
            self, id=self.CODE_BUTTON_CONFIRM, label=tve.BUTTON_CONFIRM_UPDATE_PASSWORD,
            pos=wx.DefaultPosition, size=wx.DefaultSize, style=0
        )
        self.buttonConfirm.SetFont(
            wx.Font(
                11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerRulesAndButton.Add(self.buttonConfirm, 0, wx.ALL | wx.EXPAND, 5)

        bSizerMain.Add(bSizerRulesAndButton, 1, wx.EXPAND, 5)

        self.SetSizer(bSizerMain)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_BUTTON, self.ChangePassword, id=self.CODE_BUTTON_CONFIRM)

        self.fieldOldPwd.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.fieldNewPwd.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.fieldConfirmPwd.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)

        self.fieldOldPwd.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
        self.fieldNewPwd.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
        self.fieldConfirmPwd.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)

    def __del__(self):
        pass

    def ChangePassword(self, event):
        oldPwd = self.fieldOldPwd.GetLineText(0)
        newPwd = self.fieldNewPwd.GetLineText(0)
        confirmNewPwd = self.fieldConfirmPwd.GetLineText(0)
        correctPwd = 1 if self.response['is_pwd_rules'] == 0 else 0
        oldPwdHash = None if (oldPwd == "") or (oldPwd is None) \
            else self.hash_in_md5(oldPwd)
        if oldPwdHash == self.response["password_hash"]:
            if not correctPwd:
                if re.search(self.response["re_pwd"], newPwd) or (self.response["re_pwd"] is None):
                    correctPwd = 1
                else:
                    correctPwd = 0
                    self.PwdMsg(
                        tve.MSG_FAILED_PASSWORD_RULES,
                        tve.NAME_WINDOW_ERROR_UPDATE_PASSWORD
                    )
        else:
            correctPwd = 0
            self.PwdMsg(
                tve.MSG_FAILED_OLD_PASSWORD,
                tve.NAME_WINDOW_ERROR_UPDATE_PASSWORD
            )
        if correctPwd:
            print(confirmNewPwd, " == ", newPwd)
            if confirmNewPwd == newPwd:
                newPwd = self.hash_in_md5(newPwd)
                self.db.update_password_hash_by_login(self.response['login'], newPwd)
                self.PwdMsg(
                    tve.MSG_SUCCESSFULLY_PASSWORD,
                    tve.NAME_WINDOW_SUCCESSFULLY_PASSWORD
                )
                self.UpdateStatusIsNew()
                self.GoToOpenAuthPwd()
            else:
                self.PwdMsg(
                    tve.MSG_FAILED_PASSWORD_CONFIRM,
                    tve.NAME_WINDOW_ERROR_UPDATE_PASSWORD
                )

    def GetTextRules(self):
        if (self.response['text_pwd_rules'] is None) and \
                (self.response['is_pwd_rules'] == 1):
            if (self.response["re_pwd"] is None) or \
                    (self.response["re_pwd"] == ""):
                return tve.MSG_NO_RULES_PASSWORD
            else:
                return tve.MSG_NO_TEXT_RULES_PASSWORD
        else:
            if self.response['is_pwd_rules'] == 0:
                return tve.MSG_NO_RULES_PASSWORD
            else:
                return self.response['text_pwd_rules']

    @staticmethod
    def PwdMsg(msg, window_name):
        return wx.MessageBox(
            msg, window_name, wx.OK | wx.OK_DEFAULT
        )

    def UpdateStatusIsNew(self):
        self.db.update_user_is_new_by_login(
            0, self.response['login']
        )

    def GoToOpenAuthPwd(self):
        frame = AuthFrame(None)
        frame.Show()
        self.Close()


class PersonalAreaFrame(UpdatePasswordFrame):
    CODE_EXIT_TO_AUTH = 300
    CODE_CHANGE_PWD = 301
    CODE_UPDATE_DATA = 302
    CODE_GET_UPDATE_TABLE = 303
    CODE_ADD_USER = 304
    CODE_DELETE_USER = 305

    def __init__(self, response, db: DBInteraction):
        wx.Frame.__init__(
            self, parent=None, id=wx.ID_ANY, title=tve.NAME_WINDOW_PERSONAL_AREA,
            pos=wx.DefaultPosition, size=wx.Size(760, 440),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
        )

        self.Show()
        self.response = response
        self.db = db
        self.all_users = self.db.get_users()

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizerMain = wx.BoxSizer(wx.VERTICAL)

        bSizerMenu = wx.BoxSizer(wx.HORIZONTAL)

        self.textLoginName = wx.StaticText(
            self, wx.ID_ANY, tve.TEXT_LOGIN_PERSONAL_AREA,
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.textLoginName.Wrap(-1)
        self.textLoginName.SetFont(
            wx.Font(
                10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerMenu.Add(self.textLoginName, 0, wx.ALL | wx.RIGHT, 15)

        self.textLoginValue = wx.StaticText(
            self, wx.ID_ANY, self.response['login'],
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.textLoginValue.Wrap(-1)
        bSizerMenu.Add(self.textLoginValue, 0, wx.ALL, 15)

        self.textRightsName = wx.StaticText(
            self, wx.ID_ANY, tve.TEXT_RIGHTS_PERSONAL_AREA,
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.textRightsName.Wrap(-1)
        self.textRightsName.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerMenu.Add(self.textRightsName, 0, wx.ALL, 15)

        self.textRightsValue = wx.StaticText(
            self, wx.ID_ANY, self.define_rights(),
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.textRightsValue.Wrap(-1)
        bSizerMenu.Add(self.textRightsValue, 0, wx.ALL, 15)

        self.buttonChangePwd = wx.Button(
            self, self.CODE_CHANGE_PWD, tve.BUTTON_UPDATE_PASSWORD,
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.buttonChangePwd.SetFont(
            wx.Font(
                10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerMenu.Add(self.buttonChangePwd, 1, wx.ALL, 15)

        self.buttonExitAuth = wx.Button(
            self, self.CODE_EXIT_TO_AUTH, tve.BUTTON_EXIT_PERSONAL_AREA,
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.buttonExitAuth.SetFont(
            wx.Font(
                10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerMenu.Add(self.buttonExitAuth, 1, wx.ALL, 15)

        bSizerMain.Add(bSizerMenu, 0, wx.EXPAND, 5)

        if self.response['is_admin']:
            bSizerTableUsers = wx.BoxSizer(wx.VERTICAL)

            self.dataViewList = wx.dataview.DataViewListCtrl(
                self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0
            )
            self.fillInTable(is_primary_filling=True)

            bSizerTableUsers.Add(self.dataViewList, 1, wx.ALL | wx.EXPAND, 5)

            bSizerMain.Add(bSizerTableUsers, 1, wx.EXPAND, 5)

            bSizerButtonUser = wx.BoxSizer(wx.HORIZONTAL)

            self.buttonCreateUser = wx.Button(
                self, self.CODE_ADD_USER, tve.BUTTON_ADD_USER,
                wx.DefaultPosition, wx.DefaultSize, 0
            )
            self.buttonCreateUser.SetFont(
                wx.Font(
                    10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                    wx.FONTWEIGHT_BOLD, False, wx.EmptyString
                )
            )
            bSizerButtonUser.Add(self.buttonCreateUser, 1, wx.ALL | wx.EXPAND, 5)

            self.buttonDeleteUser = wx.Button(
                self, self.CODE_DELETE_USER, tve.BUTTON_DELETE_USER,
                wx.DefaultPosition, wx.DefaultSize, 0
            )
            self.buttonDeleteUser.SetFont(
                wx.Font(
                    10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                    wx.FONTWEIGHT_BOLD, False, wx.EmptyString
                )
            )
            bSizerButtonUser.Add(self.buttonDeleteUser, 1, wx.ALL | wx.EXPAND, 5)

            self.buttonUpdateTable = wx.Button(
                self, self.CODE_GET_UPDATE_TABLE, tve.BUTTON_UPDATE_USER,
                wx.DefaultPosition, wx.DefaultSize, 0
            )
            self.buttonUpdateTable.SetFont(
                wx.Font(
                    10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                    wx.FONTWEIGHT_BOLD, False, wx.EmptyString
                )
            )
            bSizerButtonUser.Add(
                self.buttonUpdateTable, 1, wx.ALL | wx.EXPAND, 5
            )

            self.buttonUpdateCompleted = wx.Button(
                self, self.CODE_UPDATE_DATA, tve.BUTTON_SAVE_UPDATE,
                wx.DefaultPosition, wx.DefaultSize, 0
            )
            self.buttonUpdateCompleted.SetFont(
                wx.Font(
                    10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                    wx.FONTWEIGHT_BOLD, False, wx.EmptyString
                )
            )
            self.buttonUpdateCompleted.SetForegroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT)
            )
            self.buttonUpdateCompleted.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK)
            )

            bSizerButtonUser.Add(
                self.buttonUpdateCompleted, 1, wx.ALL | wx.EXPAND, 5
            )

            bSizerMain.Add(bSizerButtonUser, 0, wx.EXPAND, 5)

        self.SetSizer(bSizerMain)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_BUTTON, self.exitToAuth, id=self.CODE_EXIT_TO_AUTH)
        self.Bind(wx.EVT_BUTTON, self.changePwd, id=self.CODE_CHANGE_PWD)
        if self.response['is_admin']:
            self.Bind(wx.EVT_BUTTON, self.GetDataFromTable, id=self.CODE_UPDATE_DATA)
            self.Bind(wx.EVT_BUTTON, self.updateDataFromTable, id=self.CODE_GET_UPDATE_TABLE)
            self.Bind(wx.EVT_BUTTON, self.addNewUser, id=self.CODE_ADD_USER)
            self.Bind(wx.EVT_BUTTON, self.deleteUser, id=self.CODE_DELETE_USER)

    def __del__(self):
        pass

    def define_rights(self):
        if self.response['is_admin'] == 1:
            return tve.TEXT_RIGHTS_ADMIN
        return tve.TEXT_RIGHTS_USER

    def exitToAuth(self, event):
        self.GoToOpenAuthPwd()

    def changePwd(self, event):
        self.OpenNewPwdWindow(self.response, self.db)

    def updateDataFromTable(self, event):
        self.dataViewList.DeleteAllItems()
        self.all_users = self.db.get_users()
        self.fillInTable()
        self.response = self.db.get_user(
            self.response['login']
        )[0]

    def fillInTable(self, is_primary_filling=False):
        if is_primary_filling:
            for column_name in self.response.keys():
                mode = wx.dataview.DATAVIEW_CELL_EDITABLE if (column_name != "user_id") \
                    else wx.dataview.DATAVIEW_CELL_INERT
                self.dataViewList.AppendTextColumn(
                    column_name, mode=mode
                )
        for i in self.all_users:
            item = list(tuple(i))
            item = self.ColumnIntToStr(item)
            self.dataViewList.AppendItem(item)

    def addNewUser(self, event):
        defaultDataNewUser = [
            None, "<new user>", None,
            "0", "0", "1", "0", None, None
        ]
        self.dataViewList.AppendItem(defaultDataNewUser)

    def GetDataFromTable(self, event):
        for row in range(len(self.all_users)):
            row_item = self.get_in_the_line(row)
            if collections.Counter(row_item) != self.all_users[row]:
                value_dict = dict(zip(self.response.keys(), row_item))
                value_dict.pop('user_id')
                login = value_dict.pop('login')
                self.db.update_user_by_login(login, value_dict)
        if len(self.all_users) != self.dataViewList.GetItemCount():
            for row in range(len(self.all_users), self.dataViewList.GetItemCount()):
                row_item = self.get_in_the_line(row)
                value_dict = dict(zip(self.response.keys(), row_item))
                if self.CheckNewUserData(value_dict):
                    value_dict.pop('user_id')
                    self.db.add_user(value_dict)
                    self.updateDataFromTable(None)

    def get_in_the_line(self, row):
        row_item = []
        for column in range(len(self.response.keys())):
            row_item.append(self.dataViewList.GetTextValue(row, column))
        row_item = self.ColumnIntToStr(row_item, True)
        return row_item

    def getAllLoginUsers(self):
        list_login = []
        all_login = self.db.get_all_login()
        for login in all_login:
            list_login.append(login['login'])
        return list_login

    def CheckNewUserData(self, value_dict):
        if not (value_dict['login'] in self.getAllLoginUsers()):
            if value_dict["is_admin"] is None or value_dict["is_admin"] == "" or \
                    value_dict["is_block"] is None or value_dict["is_block"] == "" or \
                    value_dict["is_new"] is None or value_dict["is_new"] == "" or \
                    value_dict["is_pwd_rules"] is None or value_dict["is_pwd_rules"] == "" or \
                    value_dict["login"] is None or value_dict["login"] == "":
                self.PwdMsg(tve.MSG_EMPTY_FIELD, tve.NAME_WINDOW_ERROR_UPDATE_DATA)
                return False
            else:
                return True
        else:
            self.PwdMsg(tve.MSG_NON_UNIQUE_LOGIN, tve.NAME_WINDOW_ERROR_UPDATE_DATA)
            return False

    def ColumnIntToStr(self, list_item: list, reverse=False):
        columns_numerical = [0, 3, 4, 5, 6]
        if reverse:
            if list_item[2] == "":
                list_item[2] = None
            for i in columns_numerical[-1:]:
                list_item[i] = int(list_item[i])
        else:
            for i in columns_numerical:
                list_item[i] = str(list_item[i])
        return list_item

    def deleteUser(self, event):
        row = self.dataViewList.GetSelectedRow()
        if row is wx.NOT_FOUND:
            self.PwdMsg(tve.MSG_NO_SELECT_ROW, tve.NAME_WINDOW_ERROR_DELETE_USER)
        else:
            login = self.dataViewList.GetTextValue(row, 1)
            if login == self.response['login']:
                self.PwdMsg(tve.MSG_NO_DELETE_SELF, tve.NAME_WINDOW_ERROR_DELETE_USER)
            else:
                self.db.delete_user_by_login(login)
                self.updateDataFromTable(None)
