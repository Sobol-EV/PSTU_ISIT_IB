import re
from collections import Counter
from matplotlib import pyplot as plt
import numpy as np
from caesars_cipher import CaesarsCipher


class CryptanalysisText:

    characters_rus = 'абвгдежзийклмнопрстуфхцчшщыьэюя '

    __frequencies_for_russian = {
        " ": 0.175, "о": 0.09, "е": 0.072, "а": 0.062, "и": 0.062, "т": 0.053,
        "н": 0.053, "с": 0.045, "р": 0.04, "в": 0.038, "л": 0.035, "к": 0.028,
        "м": 0.026, "д": 0.025, "п": 0.023, "у": 0.021, "я": 0.018, "ы": 0.016,
        "з": 0.016, "ь": 0.014, "б": 0.014, "г": 0.013, "ч": 0.012, "й": 0.01,
        "х": 0.009, "ж": 0.007, "ю": 0.006, "ш": 0.004, "ц": 0.003, "щ": 0.003,
        "э": 0.003, "ф": 0.002
    }

    def __init__(self, path):
        import matplotlib
        matplotlib.use('TkAgg')
        self.path = path
        self.encrypted_text = self.read_cipher_from_file()
        self.frequencies = self.calc_frequencies()
        self.frequencies_double = self.calc_frequencies_double()

    def read_cipher_from_file(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                result = ""
                s = file.readlines()
                for i in s:
                    result += i.replace("\n", " ").lower()
                return result
        except FileNotFoundError:
            print("Невозможно считать файл")

    def calc_frequencies(self):
        frequencies = Counter(self.encrypted_text)
        characters = len(self.encrypted_text)
        for key in frequencies.keys():
            frequencies[key] = frequencies[key] / characters
        frequencies = dict(frequencies)
        temp_frequencies = frequencies.copy()
        for key in temp_frequencies.keys():
            if not (key in self.characters_rus):
                frequencies.pop(key)
        sorted_dictionary = {}
        for i in sorted(
                frequencies.items(), key=lambda para: para[1], reverse=True
        ):
            sorted_dictionary[i[0]] = i[1]
        for i in self.__frequencies_for_russian.keys():
            if i in sorted_dictionary.keys():
                pass
            else:
                sorted_dictionary[i] = 0
        # print(sorted_dictionary)
        return sorted_dictionary

    def calc_frequencies_double(self):
        m = []
        d_find = {}
        for key in self.frequencies.keys():
            m.append(key * 2)
        for i in m:
            count = self.count_substrings(self.encrypted_text, i)
            if count > 0:
                d_find[i] = count
        return d_find

    @staticmethod
    def count_substrings(string, substring):
        substring_re = '(?=(%s))' % re.escape(substring)
        return len(re.findall(substring_re, string))

    @staticmethod
    def __draw_histogram(counter, ax=None):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        frequencies = list(counter.values())
        names = list(counter.keys())
        x_coordinates = np.arange(len(counter))
        ax.bar(x_coordinates, frequencies, align='center')
        ax.xaxis.set_major_locator(plt.FixedLocator(x_coordinates))
        ax.xaxis.set_major_formatter(plt.FixedFormatter(names))
        return ax

    def draw_hist_letters(self):
        self.__draw_histogram(self.frequencies)
        plt.show()

    def draw_hist_double_letters(self):
        self.__draw_histogram(self.frequencies_double)
        plt.show()

    def full_frequency_matching(self):
        """НЕ ИСПОЛЬЗОВАЛ Т.K МЕНЕЕ ЭФФЕКТИВНЫЙ"""
        ras = []
        dictinary = dict(
            zip(
                self.frequencies.keys(),
                self.__frequencies_for_russian.keys()
            )
        )
        for symbol in self.encrypted_text:
            ras.append(dictinary.get(symbol, " "))
        text = "".join(ras)
        return text

    def all_possible_keys(self):
        cipher_c = CaesarsCipher()
        result_key = []
        result = []
        m_possible_keys = []
        index = 0
        for reference_value in self.__frequencies_for_russian.keys():
            # print(list(self.frequencies.keys()))
            # print("INDEX: ", index)
            ac_value = self.characters_rus.find(
                list(self.frequencies.keys())[index]
            )
            # print(ac_value)
            ref_value = self.characters_rus.find(reference_value)
            if ac_value < ref_value:
                m_possible_keys.append(
                    len(self.characters_rus) - ref_value + ac_value
                )
            else:
                m_possible_keys.append(ac_value - ref_value)
            index += 1
        count_possible_keys = dict(Counter(m_possible_keys))
        max_count = max(count_possible_keys.values())
        for key in count_possible_keys:
            if count_possible_keys[key] == max_count:
                result_key.append(key)
        for key in result_key:
            result.append(
                cipher_c.cipher(
                    key, self.encrypted_text, 'decrypt'
                )
            )
        for text in result:
            print(text)
        print(m_possible_keys)
        return result

path = "../text_files/encC_source_text.txt"
# path = input("Укажите путь до файла зашифрованного методом Цезаря: ")
c_hacker = CryptanalysisText(path)
c_hacker.draw_hist_letters()
c_hacker.draw_hist_double_letters()
c_hacker.all_possible_keys()
