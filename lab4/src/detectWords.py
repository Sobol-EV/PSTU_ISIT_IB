
class DetectedWords:

    UPPER_LETTERS_ENG = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    UPPER_LETTERS_RUS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    PATH_DICTIONARY_RUS = 'dictionaries_for_enumeration/russian_nouns.txt'
    PATH_DICTIONARY_ENG = 'dictionaries_for_enumeration/english.txt'

    def __init__(self, message, language="rus"):
        self.language = language
        self.message = message
        if language == "eng":
            self.LETTERS_AND_SPACE = self.UPPER_LETTERS_ENG + \
                                     self.UPPER_LETTERS_ENG.lower() + ' \t\n'
            self.path_dictionary = self.PATH_DICTIONARY_ENG
        if language == "rus":
            self.LETTERS_AND_SPACE = self.UPPER_LETTERS_RUS + \
                                     self.UPPER_LETTERS_RUS.lower() + ' \t\n'
            self.path_dictionary = self.PATH_DICTIONARY_RUS
        self.words = self.loadDictionaryWords()

    def loadDictionaryWords(self):
        dictionary_file = open(self.path_dictionary, encoding='utf-8')
        words = {}
        for word in dictionary_file.read().split('\n'):
            words[word] = None
        dictionary_file.close()
        return words

    def getCountSignificantWords(self, message):
        message = message.lower()
        message = self.removeNonLetters(message)
        possible_words = message.split()
        if possible_words == []:
            return 0.0  # слова отсутствуют, поэтому возвращаем О.О
        matches = 0
        for word in possible_words:
            if word in self.words:
                matches += 1
        return float(matches) / len(possible_words)

    def removeNonLetters(self, message):
        letters_only = []
        for symbol in message:
            if symbol in self.LETTERS_AND_SPACE:
                letters_only.append(symbol)
        return ''.join(letters_only)

    def isMeaningfulWords(self, word_percentage=15, letter_percentage=85):
        """
        По умолчанию 15% слов должны быть в файле словаря,
        а 85% символов сообщения должны быть буквами или
        пробелами (а не знаками препинания или числами).
        """
        words_match = self.getCountSignificantWords(self.message) * 100 >= word_percentage
        num_letters = len(self.removeNonLetters(self.message))
        message_letters_percentage = float(num_letters) / len(self.message) * 100
        letters_match = message_letters_percentage >= letter_percentage
        return words_match and letters_match
