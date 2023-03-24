
class CaesarsCipher:

    @staticmethod
    def cipher(key, message, mode):
        message = message.lower()
        SYMBOLS = 'абвгдежзийклмнопрстуфхцчшщыьэюя '
        translated = ''
        for symbol in message:
            translatedIndex = None
            if symbol in SYMBOLS:
                symbolIndex = SYMBOLS.find(symbol)
                if mode == 'encrypt':
                    translatedIndex = symbolIndex + key
                elif mode == 'decrypt':
                    translatedIndex = symbolIndex - key
                if translatedIndex >= len(SYMBOLS):
                    translatedIndex = translatedIndex - len(SYMBOLS)
                elif translatedIndex < 0:
                    translatedIndex = translatedIndex + len(SYMBOLS)
                translated = translated + SYMBOLS[translatedIndex]
            else:
                translated = translated + symbol

        return translated
