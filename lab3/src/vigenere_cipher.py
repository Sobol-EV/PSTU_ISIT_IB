from random import shuffle


class VigenereCipher:
    """
    Шифр Виженера - модуль шифрования/дешифрования
    """

    def __init__(
            self, code, path_file_input,
            path_file_output_enc, path_file_output_dec, mix
    ):
        self.code = code
        self.tmp_alphabet = None
        self.path_file_input = path_file_input
        self.path_file_output_enc = path_file_output_enc
        self.path_file_output_dec = path_file_output_dec
        self.mix = mix
        self.reading_and_writing_from_file(
            k=self.code, r=self.path_file_input,
            w=self.path_file_output_enc, dec=False,
            mix=self.mix
        )
        self.reading_and_writing_from_file(
            k=self.code, r=self.path_file_output_enc,
            w=self.path_file_output_dec, dec=True
        )

    DEFAULT_LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    # Словарь по умолчанию( Массив с набором используемых символов)

    LETTERS = ""

    def mix_alphabet(self):
        words = self.DEFAULT_LETTERS.split()
        for i, word in enumerate(map(list, words)):
            shuffle(word)
            words[i] = ''.join(word)
        return str(*words)

    def encryptMessage(self, key, message, mix):
        return self.translateMessage(key, message, 'encrypt', mix)

    def decryptMessage(self, key, message):
        return self.translateMessage(key, message, 'decrypt', None, self.LETTERS)

    def translateMessage(self, key, message, mode, mix, alphabet=None):
        translated = []  # хранит зашифрованное /дешифрованное сообщение
        key_index = 0
        key = key.upper()
        if alphabet:
            self.LETTERS = alphabet
        else:
            if mode == 'encrypt':
                self.LETTERS = self.DEFAULT_LETTERS if not mix else self.mix_alphabet()
            if mode == 'decrypt':
                if self.LETTERS is None or self.LETTERS == "":
                    self.LETTERS = self.DEFAULT_LETTERS
        # print(mode, "------> ", self.LETTERS, " alf:", alphabet)
        # print("Сообщение: ", message)
        for symbol in message:  # цикл по символам строки message
            # print("-------------------------------------Символ:", symbol)
            num = self.LETTERS.find(symbol.upper())
            # print("Место:", num, end="")
            if num != -1:  # -1 means symbol.upper() найден в строке LETTERS.
                if mode == 'encrypt':
                    num += self.LETTERS.find(key[key_index])  # Добавить в случае шифрования
                    # print(" --> ", num)
                elif mode == 'decrypt':
                    num -= self.LETTERS.find(key[key_index])  # Вычесть в случае дешифрования
                    # print(" --> ", num)
                num %= len(self.LETTERS)  # обработка завертывания
                # print("ПОЗИЦИЯ: ", num)
                # Добавить зашифрованный/дешифрованный символ в конец
                # print("Перед сравнением: ", self.LETTERS[num])
                if symbol.isupper():
                    translated.append(self.LETTERS[num])
                    # print("ДОБАВЛЯЕМ СИМВОЛ: ", self.LETTERS[num])
                    # print("--> ", translated)
                elif symbol.islower():
                    translated.append(self.LETTERS[num].lower())
                    # print("ДОБАВЛЯЕМ СИМВОЛ: ", self.LETTERS[num])
                    # print("--> ", translated)
                key_index += 1  # перейти к следующей букве ключа
                if key_index == len(key):
                    key_index = 0
            else:
                # Присоединить символ без шифрования/дешифрования
                translated.append(symbol)
            # print("ИТОГ: ", ''.join(translated))
        return ''.join(translated)

    # Функция считывания, записи и шифрования
    # 1- кодовое слово, 2- файл прочитать, 3- файл куда записать 4 - шифр\дешифр, 5 -шифров/дешифр
    def reading_and_writing_from_file(self, k, r, w, dec, mix=False):
        # Открываю файл на чтение
        file_to_read = open(r, encoding='utf-8')
        # Открываю файл на запись
        file_for_writing = open(w, 'w', encoding='utf-8')
        # Считываю построчно из файла
        for line in file_to_read:
            l = line
            # Удаляю знак переноса строки
            l = l[:-1] if l.find("\n") != -1 else l
            # Записываю в файл строку
            if dec:
                file_for_writing.write(str(self.decryptMessage(k, l)) + '\n')
            else:
                file_for_writing.write(str(self.encryptMessage(k, l, mix) + '\n'))
        # Закрываю файл на запись
        file_for_writing.close()
        # Закрываю файл на чтение
        file_to_read.close()

test = VigenereCipher(
    "шифр",
    "../text_files/source_text.txt",
    "../text_files/encV_source_text.txt",
    "../text_files/decV_source_text.txt",
    False
)
