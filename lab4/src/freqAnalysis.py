

class FrequencyAnalysis:

    FREQ_STANDARD_ENG = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    LETTERS_ENG = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    FREQ_STANDARD_RUS = 'ОЕАИНТСРВЛКМДПУЯЫЬГЗБЧЙХЖШЮЦЩЭФЪЁ'
    LETTERS_RUS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    LETTER_COUNT_RUS = {
        'А': 0, 'Б': 0, 'В': 0, 'Г': 0, 'Д': 0, 'Е': 0, 'Ё': 0, 'Ж': 0,
        'З': 0, 'И': 0, 'Й': 0, 'К': 0, 'Л': 0, 'М': 0, 'Н': 0,
        'О': 0, 'П': 0, 'Р': 0, 'С': 0, 'Т': 0, 'У': 0, 'Ф': 0,
        'Х': 0, 'Ц': 0, 'Ч': 0, 'Ш': 0, 'Щ': 0, 'Ъ': 0, 'Ы': 0, 'Ь': 0,
        'Э': 0, 'Ю': 0, 'Я': 0
    }
    LETTER_COUNT_ENG = {
        'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0,
        'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0,
        'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0,
        'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0
    }

    def __init__(self, message: str, language="rus"):
        self.message = message
        self.language = language
        if language == "rus":
            self.FREQ_STANDARD = self.FREQ_STANDARD_RUS
            self.LETTERS = self.LETTERS_RUS
            self.LETTER_COUNT = self.LETTER_COUNT_RUS
            # print(self.message)
        if language == "eng":
            self.FREQ_STANDARD = self.FREQ_STANDARD_ENG
            self.LETTERS = self.LETTERS_ENG
            self.LETTER_COUNT = self.LETTER_COUNT_ENG

    def getLetterCount(self):
        """
        Возвращает словарь , ключами которого являются буквы ,
        а значениями - частотность каждой буквы в строке message
        """
        for letter in self.message.upper():
            if letter in self.LETTERS:
                self.LETTER_COUNT[letter] += 1
        # print(self.LETTER_COUNT)
        return self.LETTER_COUNT

    @staticmethod
    def getItemAtIndexZero(items):
        return items[0]

    def getFrequencyOrder(self):
        """
        Возвращает строку букв алфавита, расположенных в порядке
        убывания их частотности в строке message.
        """
        # Получаем словарь частотности букв
        letter_to_freq = self.getLetterCount()
        # Создаем словарь счетчиков частотности со списком букв по каждому счетчику
        freq_to_letter = {}
        for letter in self.LETTERS:
            if letter_to_freq[letter] not in freq_to_letter:
                freq_to_letter[letter_to_freq[letter]] = [letter]
            else:
                freq_to_letter[letter_to_freq[letter]].append(letter)
        # Изменяем порядок букв в каждом списке на обратный
        # порядку " ETAOIN" и превращаем списки в строки
        for freq in freq_to_letter:
            freq_to_letter[freq].sort(key=self.FREQ_STANDARD.find, reverse=True)
            freq_to_letter[freq] = ''.join(freq_to_letter[freq])
        # Преобразуем словарь freqToLetter в список
        # кортежей (ключ, значение) и сортируем его
        freq_pairs = list(freq_to_letter.items())
        freq_pairs.sort(key=self.getItemAtIndexZero, reverse=True)
        # После того, как буквы были упорядочены по частотности ,
        # извлекаем все буквы для формирования окончательной строки.
        freq_order = []
        for freqPair in freq_pairs:
            freq_order.append(freqPair[1])
        # print(''.join(freq_order))
        return ''.join(freq_order)

    def FreqMatchScore(self):
        """
        Возвращает оценку частотного соответствия для строки
        message . Совпадения проверяются по шести наиболее
        и наименее часто встречающимся буквам в строке
        и в языке в целом .
        """
        freq_order = self.getFrequencyOrder()
        print("---------------------------------")
        print("ЭТАЛОН->   ", self.FREQ_STANDARD)
        print("ПОЛУЧЕНО-> ", freq_order)
        match_score = 0
        # Число совпадений для шести наиболее часто в стречающихся букв
        for common_letter in self.FREQ_STANDARD[:6]:
            if common_letter in freq_order[:6]:
                print(common_letter, end="")
                match_score += 1
            else:
                print("*", end="")
        print()
        # Число совпадений для шести наименее часто встречающихся букв
        for uncommon_letter in self.FREQ_STANDARD[-6:]:
            if uncommon_letter in freq_order[-6:]:
                print(uncommon_letter, end="")
                match_score += 1
            else:
                print("*", end="")
        print()
        print("ИТОГО: ", match_score)
        return match_score

