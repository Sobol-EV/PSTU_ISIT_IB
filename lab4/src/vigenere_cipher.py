

class VigenereCipher:
    """
    Шифр Виженера модуль шифрования/дешифрования.
    """

    LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    # Словарь по умолчанию( Массив с набором используемых символов)

    def encryptMessage(self, key, message):
        return self.translateMessage(key, message, 'encrypt')

    def decryptMessage(self, key, message):
        return self.translateMessage(key, message, 'decrypt')

    def translateMessage(self, key, message: str, mode):
        translated = []  # хранит зашифрованное /дешифрованное сообщение
        key_index = 0
        key = key.upper()
        for symbol in message:  # цикл по символам строки message
            num = self.LETTERS.find(symbol.upper())
            if num != -1:  # -1 means symbol.upper() найден в строке LETTERS.
                if mode == 'encrypt':
                    num += self.LETTERS.find(key[key_index])  # Добавить в случае шифрования
                elif mode == 'decrypt':
                    num -= self.LETTERS.find(key[key_index])  # Вычесть в случае дешифрования
                num %= len(self.LETTERS)  # обработка завертывания
                # Добавить зашифрованный/дешифрованный символ в конец
                if symbol.isupper():
                    translated.append(self.LETTERS[num])
                elif symbol.islower():
                    translated.append(self.LETTERS[num].lower())
                key_index += 1  # перейти к следующей букве ключа
                if key_index == len(key):
                    key_index = 0
            else:
                # Присоединить символ без шифрования/дешифрования
                translated.append(symbol)
        return ''.join(translated)

# a = VigenereCipher()
# print(a.encryptMessage("тест", "Тестовое сообщение"))
# print("---------------------------------------------------------")
# print(a.decryptMessage("тест", a.encryptMessage("тест", "Тестовое сообщение")))
