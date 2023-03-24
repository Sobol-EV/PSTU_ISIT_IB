
class CaesarsCipher:

    def __init__(self, path_input, path_output_enc, path_output_dec, key):
        self.key = key
        self.key = abs(key)
        self.path_input = path_input
        self.path_output_enc = path_output_enc
        self.path_output_dec = path_output_dec
        self.encryption(self.path_input, self.path_output_enc, mode='encrypt')
        self.encryption(self.path_output_enc, self.path_output_dec, mode='decrypt')

    def cipher(self, message, mode):
        # message = message.lower()
        SYMBOLS = 'абвгдежзийклмнопрстуфхцчшщыьэюя '
        translated = ''

        for symbol in message:
            translatedIndex = None
            if symbol.lower() in SYMBOLS:
                symbolIndex = SYMBOLS.find(symbol.lower())

                if mode == 'encrypt':
                    translatedIndex = symbolIndex + self.key
                elif mode == 'decrypt':
                    translatedIndex = symbolIndex - self.key

                if translatedIndex >= len(SYMBOLS):
                    translatedIndex = translatedIndex - len(SYMBOLS)
                elif translatedIndex < 0:
                    translatedIndex = translatedIndex + len(SYMBOLS)

                if symbol.isupper():
                    translated = translated + SYMBOLS[translatedIndex].upper()
                elif symbol.islower() or " ":
                    translated = translated + SYMBOLS[translatedIndex]
            else:
                translated = translated + symbol

        return translated

    def encryption(self, r, w, mode='encrypt'):
        # Открываю файл на чтение
        f = open(r, encoding='utf-8')
        # Открываю файл на запись
        w1 = open(w, 'w', encoding='utf-8')
        # Считываю построчно из файла
        for line in f:
            l = line
            # Удаляю знак переноса строки
            l = l[:-1] if l.find("\n") != -1 else l
            # Записываю в файл зашифрованную строку
            if mode == 'encrypt':
                l.replace("ё", "е").replace("ъ", "ь").replace("Ё", "ё").lower()
            elem = str(self.cipher(l, mode=mode))
            w1.write(elem + '\n')
        # Закрываю файл на запись
        w1.close()
        # Закрываю файл на чтение
        f.close()

