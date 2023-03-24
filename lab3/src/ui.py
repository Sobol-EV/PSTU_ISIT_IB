import wx
import wx.xrc
import wx.richtext
from vigenere_cipher import VigenereCipher
from caesars_cipher import CaesarsCipher


class MainFrame(wx.Frame):

    CODE_CHOICE_ADDITIONAL_OPTIONS = 100
    CODE_CHOICE_SELECT_METHOD = 101
    CODE_FILE_PATH_OUTPUT = 102
    CODE_BUTTON_OPEN_SOURCE_FILE = 103
    CODE_BUTTON_START_ENCRYPTION = 104

    def __init__(self, parent):
        wx.Frame.__init__(
            self, parent, id=wx.ID_ANY, title="Шифрование",
            pos=wx.DefaultPosition, size=wx.Size(1106, 648),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizerMain = wx.BoxSizer(wx.VERTICAL)

        bSizerMenu = wx.BoxSizer(wx.HORIZONTAL)

        self.TextEncryptionMethod = wx.StaticText(
            self, wx.ID_ANY, u"Выбирите метод шифрования: ",
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.TextEncryptionMethod.Wrap(-1)
        self.TextEncryptionMethod.SetFont(
            wx.Font(
                10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerMenu.Add(self.TextEncryptionMethod, 0, wx.ALL, 5)

        ListEncryptionMethodValues = ["Метод Виженера", "Метод Цезаря"]
        self.ListEncryptionMethod = wx.Choice(
            self, self.CODE_CHOICE_SELECT_METHOD, wx.DefaultPosition,
            wx.DefaultSize, ListEncryptionMethodValues, 0
        )
        self.ListEncryptionMethod.SetSelection(0)
        bSizerMenu.Add(self.ListEncryptionMethod, 0, wx.ALL, 5)

        self.TextAdditionalOptions = wx.StaticText(
            self, wx.ID_ANY, u"Дополниельные опции:",
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.TextAdditionalOptions.Wrap(-1)
        self.TextAdditionalOptions.SetFont(
            wx.Font(
                10, wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD,
                False, wx.EmptyString
            )
        )
        bSizerMenu.Add(self.TextAdditionalOptions, 0, wx.ALL, 5)
        self.ListAdditionalOptionsValues = []
        if self.ListEncryptionMethod.GetCurrentSelection() == 0:
            self.ListAdditionalOptionsValues = ["Словарь (случайный)", "Словарь (по порядку)"]
        else:
            self.ListEncryptionMethodValues = ["Опций нет"]
        self.ListAdditionalOptions = wx.Choice(
            self, wx.ID_ANY, wx.DefaultPosition,
            wx.DefaultSize, self.ListAdditionalOptionsValues, 0
        )
        self.ListAdditionalOptions.SetSelection(0)
        bSizerMenu.Add(self.ListAdditionalOptions, 0, wx.ALL, 5)

        self.TextFileToEncrypt = wx.StaticText(
            self, wx.ID_ANY, u"Исходный файл: ",
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.TextFileToEncrypt.Wrap(-1)
        self.TextFileToEncrypt.SetFont(
            wx.Font(
                10, wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD,
                False, wx.EmptyString
            )
        )
        bSizerMenu.Add(self.TextFileToEncrypt, 0, wx.ALL, 5)

        self.FileToEncryptOutput = wx.TextCtrl(
            self, self.CODE_FILE_PATH_OUTPUT, wx.EmptyString,
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        bSizerMenu.Add(self.FileToEncryptOutput, 1, wx.ALL, 5)

        self.ButtonFileToEncrypt = wx.Button(
            self, self.CODE_BUTTON_OPEN_SOURCE_FILE, u"Выбрать",
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.ButtonFileToEncrypt.SetFont(
            wx.Font(
                10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerMenu.Add(self.ButtonFileToEncrypt, 0, wx.ALL, 5)

        bSizerMain.Add(bSizerMenu, 0, wx.EXPAND, 5)

        bSizerOutputLog = wx.BoxSizer(wx.VERTICAL)

        self.OutputLog = wx.richtext.RichTextCtrl(
            self, wx.ID_ANY, wx.EmptyString,
            wx.DefaultPosition, wx.DefaultSize,
            0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS
        )
        bSizerOutputLog.Add(self.OutputLog, 1, wx.EXPAND | wx.ALL, 5)

        bSizerMain.Add(bSizerOutputLog, 1, wx.EXPAND, 5)

        bSizerButtonStart = wx.BoxSizer(wx.VERTICAL)

        bSizerCodeKey = wx.BoxSizer(wx.HORIZONTAL)

        self.TextCodeKey = wx.StaticText(
            self, wx.ID_ANY, u"Кодовое слово / сдвиг:",
            wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT
        )
        self.TextCodeKey.Wrap(-1)
        self.TextCodeKey.SetFont(
            wx.Font(
                10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerCodeKey.Add(self.TextCodeKey, 1, wx.ALL, 5)

        self.fieldCodeKey = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString,
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.fieldCodeKey.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerCodeKey.Add(self.fieldCodeKey, 2, wx.ALL, 5)

        bSizerButtonStart.Add(bSizerCodeKey, 1, wx.EXPAND, 5)

        self.buttonStart = wx.Button(
            self, self.CODE_BUTTON_START_ENCRYPTION, u"ЗАПУСТИТЬ ",
            wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.buttonStart.SetFont(
            wx.Font(
                11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC,
                wx.FONTWEIGHT_BOLD, False, wx.EmptyString
            )
        )
        bSizerButtonStart.Add(self.buttonStart, 1, wx.ALL | wx.EXPAND, 5)

        bSizerMain.Add(bSizerButtonStart, 0, wx.EXPAND, 5)

        self.SetSizer(bSizerMain)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Bind(
            wx.EVT_CHOICE,
            self.DisplayingAdditionalOptions,
            id=self.CODE_CHOICE_SELECT_METHOD
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.open_source_file,
            id=self.CODE_BUTTON_OPEN_SOURCE_FILE
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.start_encryption,
            id=self.CODE_BUTTON_START_ENCRYPTION
        )

    def __del__(self):
        pass

    @staticmethod
    def __update_choice(choice: wx.Choice, list_values: list):
        choice.Clear()
        choice.Append(list_values)
        choice.SetSelection(0)

    def DisplayingAdditionalOptions(self, event):
        if self.ListEncryptionMethod.GetCurrentSelection() == 0:
            self.__update_choice(
                self.ListAdditionalOptions,
                ["Словарь (случайный)", "Словарь (по порядку)"]
            )
        else:
            self.__update_choice(self.ListAdditionalOptions, ["-"])

    def open_source_file(self, event):
        with wx.FileDialog(
                self, "Открыть файл...", wildcard="Текстовые файлы (*.txt)|*.txt",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            self.FileToEncryptOutput.Clear()
            self.FileToEncryptOutput.AppendText(pathname)
            self.get_dir_file(pathname)

    def start_encryption(self, event):
        option = self.ListAdditionalOptions.GetCurrentSelection()
        method = self.ListEncryptionMethod.GetCurrentSelection()
        if method == 0:
            if option == 0:
                print("---СЛУЧАЙНЫЙ---")
                self.vigenere_encryption(mix=True)
            if option == 1:
                self.vigenere_encryption(mix=False)
        if method == 1:
            self.caesars_cipher()

    def caesars_cipher(self):
        original_path = self.FileToEncryptOutput.GetLineText(0)
        if original_path:
            code_key = self.fieldCodeKey.GetLineText(0)
            if code_key:
                code_key = int(code_key)
                if self.check_count_symbol_in_file(original_path):
                    path_enc = self.join_file_path_parts(original_path, "encC_")
                    path_dec = self.join_file_path_parts(original_path, "decC_")
                    cryptor = CaesarsCipher(
                        original_path,
                        path_enc,
                        path_dec,
                        code_key
                    )
                    self.OutputLog.Clear()
                    self.output_head_line(path_enc)
                    self.output_head_line(path_dec)
            else:
                self.msg("Не указан сдвиг для зашифровки!", "Ошибка!")
        else:
            self.msg("Не выбран файл для зашифровки!", "Ошибка!")

    def vigenere_encryption(self, mix=False):
        original_path = self.FileToEncryptOutput.GetLineText(0)
        if original_path:
            code_key = self.fieldCodeKey.GetLineText(0)
            if code_key:
                if self.check_count_symbol_in_file(original_path):
                    path_enc = self.join_file_path_parts(original_path, "encV_")
                    path_dec = self.join_file_path_parts(original_path, "decV_")
                    cryptor = VigenereCipher(
                        code_key,
                        original_path,
                        path_enc,
                        path_dec,
                        mix
                    )
                    self.OutputLog.Clear()
                    self.output_vigenere_square(cryptor.LETTERS)
                    self.output_head_line(path_enc)
                    self.output_head_line(path_dec)
            else:
                self.msg("Не указано кодовое слово для зашифровки!", "Ошибка!")
        else:
            self.msg("Не выбран файл для зашифровки!", "Ошибка!")

    def output_vigenere_square(self, m):
        line = None
        x = 0
        y = len(m)
        self.add_highlight_title(
            "---------------КВАДРАТ ВИЖЕНЕРА----------\n\n"
        )
        for i in range(len(m)):
            line = ""
            for j in range(x, y):
                line += m[j]
            self.OutputLog.WriteText(line + "\n")
            x -= 1
            y -= 1

    def join_file_path_parts(self, path, prefix):
        info_path = self.get_dir_file(path)
        result_path = "\\".join(
            [info_path["dir"], prefix+info_path["name"]]
        )
        return result_path

    @staticmethod
    def get_dir_file(path: str):
        m = path.split("\\")
        name = m.pop(-1)
        dir = '\\'.join(m)
        return {
            "name": name,
            "dir": dir
        }

    def output_head_line(self, path):
        self.add_highlight_title(f"-----> {path}\n")
        with open(path, encoding='utf-8') as file:
            head = [next(file) for x in range(1)]
            for line in head:
                self.OutputLog.WriteText(line + "\n")

    def add_highlight_title(self, text):
        self.OutputLog.BeginBold()
        self.OutputLog.BeginFontSize(12)
        self.OutputLog.WriteText(text)
        self.OutputLog.EndFontSize()
        self.OutputLog.EndBold()

    def check_count_symbol_in_file(self, path):
        file = open(path, "r", encoding='utf-8')
        data = file.read()
        if len(data) < 2000:
            self.msg(
                "В файле должно быть минимум 2000 символов!",
                "Ошибка!"
            )
            return False
        return True

    @staticmethod
    def msg(text, frame_name):
        return wx.MessageBox(
            text, frame_name, wx.OK | wx.OK_DEFAULT
        )

