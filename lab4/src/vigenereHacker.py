import itertools, re

import pyperclip

from freqAnalysis import FrequencyAnalysis
from detectWords import DetectedWords
from vigenere_cipher import VigenereCipher
LETTERS = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ'
SILENT_MODE = False  # True - отключение вывода
NUM_MOST_FREQ_LETTERS = 6  # ограничение количества букв на подключ
MAX_KEY_LENGTH = 4  # ограничение длины проверяемых ключей
NONLETTERS_PATTERN = re.compile('[^А-Я]')


def read_cipher_from_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            result = ""
            s = file.readlines()
            for i in s:
                result += i.replace("\n", " ").lower()
            return result
    except FileNotFoundError:
        print("Невозможно считать файл")


def main():
    # ciphertext = input("Введите зашифрованный текст: ")
    ciphertext = read_cipher_from_file("../text_files/encV_source_text.txt")
    hackedMessage = hackVigenere(ciphertext)

    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption.')


def findRepeatSequencesSpacings(message):
    """
    Находит в сообщении любые 3-х, 4-х и 5
    - буквенные повторяющиеся последовательности .
    Возвращает словарь , в котором ключи - это последовательности ,
    а значения - списки интервалов повторения .
    """
    # Используем регулярное выражение для удаления небуквенных символов
    message = NONLETTERS_PATTERN.sub('', message.upper())
    # print(message)
    # Получение списка последователь ностей, найденных в сообщении
    # ключи - последовательности , значения -списки интервалов повторения
    seq_spacings = {}
    for seq_len in range(3, 6):
        for seq_start in range(len(message) - seq_len):
            # Получение очередной последователь ности
            seq = message[seq_start:seq_start + seq_len]
            # Поиск этой последовательности в остальной части сообщения
            for i in range(seq_start + seq_len, len(message) - seq_len):
                if message[i:i + seq_len] == seq:
                    # Найдена повторяющаяся последовательность
                    if seq not in seq_spacings:
                        seq_spacings[seq] = []  # Пустой список
                    # Добавить интервал повторения между исходной и повторившейся последователь ностями
                    seq_spacings[seq].append(i - seq_start)
    print(seq_spacings)
    return seq_spacings


def getUsefulFactors(num):
    """
    Возвращает список полезных множителей параметра num.
    Полезными считаются множители от 2 до МAX_KEY_LENGTH.
    Например, вызов getUseful Factors(144)
    вернет [ 2, 3, 4, 6, 8, 9, 12, 16] .
    """
    if num < 2:
        return []  # числа , меньшие 2, не имеют полезных множителей
    factors = []  # список найденных множителей
    # При поиске множителей необходимо проверять лишь целые числа вплоть до МАХ КЕУ LENGTH
    for i in range(2, MAX_KEY_LENGTH + 1):  # множитель 1 бесполезен
        if num % i == 0:
            factors.append(i)
            other_factor = int(num / i)
            if other_factor < MAX_KEY_LENGTH + 1 and other_factor != 1:
                factors.append(other_factor)
    return list(set(factors))  # удаляем дубликаты.


def getItemAtIndexOne(items):
    return items[1]


def getMostCommonFactors(seq_factors):
    # Подсчитываем повторы множителей в словаре seqFactors
    factor_counts = {}  # ключ - множитель ; значение - число повторений
    # Ключи словаря seqFactors - это цепочки букв , а значения - списки
    # множителей интервалов повторения . Словарь выглядит примерно так :
    # { ' GFD ' : [ 2 , 3, 4, 6, 9, 1 2 , 18, 23, 36, 46, 69, 92 , 138 , 207 ], ' ALW ' : [ 2 , 3, 4 , 6 , ... ], ... }
    for seq in seq_factors:
        factor_list = seq_factors[seq]
        for factor in factor_list:
            if factor not in factor_counts:
                factor_counts[factor] = 0
            factor_counts[factor] += 1
    # Объединяем множители и счетчики повторений в кортежи
    # и создаем список таких кортежей , чтобы их можно было сортировать
    factors_by_count = []
    for factor in factor_counts:
        if factor <= MAX_KEY_LENGTH:  # Исключаем множители, которые больше, чем МАХ_КЕУ_LENGTH
            # factorsByCount - список кортежей ( множитель , счетчик ) .
            # Типичный вид : [ (3, 4 9 7 ) , (2, 4 8 7 ) , ... ]
            factors_by_count.append((factor, factor_counts[factor]))
    # Сортировка списка по счетчикам повторений
    factors_by_count.sort(key=getItemAtIndexOne, reverse=True)
    print(factors_by_count)
    return factors_by_count


def kasiskiExamination(ciphertext):
    """
    Находим последовательности длиной от 3 до 5 букв , встречающиеся
    в шифротексте неоднократно . Словарь repeatedSeqSpacings выглядит
    примерно так : { ' EXG ' : [ 192 ] , ' NAF ' : [ 339, 972, 633] , ... }
    """
    repeated_seq_spacings = findRepeatSequencesSpacings(ciphertext)
    # описание словаря seqFactors в функции getMostCommonFactors ()
    seq_factors = {}
    for seq in repeated_seq_spacings:
        seq_factors[seq] = []
        for spacing in repeated_seq_spacings[seq]:
            seq_factors[seq].extend(getUsefulFactors(spacing))
    # описание factorsByCount в функции getMostCommonFactors ()
    factors_by_count = getMostCommonFactors(seq_factors)
    # Извлекаем множители из списка factorsByCount
    # и помещаем их в список allLikelyKeyLengths , чтобы
    # с ними было проще работать
    all_likely_key_lengths = []
    for two_int_tuple in factors_by_count:
        all_likely_key_lengths.append(two_int_tuple[0])
    return all_likely_key_lengths


def getNthSubkeysLetters(nth, key_length, message):
    """
    Возвращает каждую n-ю букву из каждого набора длиной keyLength.
    Так, getNthSubkeysLetters (l, 3, ' АВСАВСАВС ') возвращает 'ААА ',
    getNthSubkeysLet ters (2, 3, ' АВСАВСАВС ') возвращает ' ВВВ ' ,
    getNthSubkeysLetters (3, 3, ' АВСАВСАВС ') возвращает ' ССС ' ,
    getNthSubkeysLetters (1, 5, ' AВCDEFGHI ') возвращает ' AF ' .
    """

    # Используем регулярное выражение для удаления небуквенных символов
    message = NONLETTERS_PATTERN.sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += key_length
    return ''.join(letters)


def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    vCipher = VigenereCipher()
    # Определяем наиболее вероятные буквы для каждого подключа
    ciphertextUp = ciphertext.upper()
    # allFreqScores - список длиной mostLikelyKeyLength,
    # элементами которого являются списки freqScores
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)

        # freqScores - список кортежей вида[(<буква>,
        # <оценка частотного соответствия>), ... ] . Список сортируется
        # по оценкам: чем выше, тем лучше . См . комментарии к функции
        # englishFreqМatchScore() в модуле freqAnalysis.py.
        freqScores = []
        for possibleKey in LETTERS:
            print(f"-------> ТЕКСТ ДЕШИФРОВАН БУКВОЙ: '{possibleKey}'")
            decryptedText = vCipher.decryptMessage(possibleKey, nthLetters)
            freqAnalysis = FrequencyAnalysis(decryptedText)
            keyAndFreqMatchTuple = (possibleKey, freqAnalysis.FreqMatchScore())
            freqScores.append(keyAndFreqMatchTuple)
        # Сортировка по оценкам частотного соответствия
        freqScores.sort(key=getItemAtIndexOne, reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])
        print("------------------------------------->", allFreqScores)

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            # Используем i+1, чтобы первая буква не считалась 0-й
            print('Возможные буквы для буквы " %s " ключа: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print()  # переход на новую строку

    # Проверяем все комбинации наиболее вероятных букв
    # для каждой позиции в ключе
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        # Создаем возможный ключ из букв в списке allFreqScores
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]

        if not SILENT_MODE:
            print('Попытка с ключом: %s' % (possibleKey))

        decryptedText = vCipher.decryptMessage(possibleKey, ciphertextUp)
        # print(decryptedText)
        detect_words = DetectedWords(decryptedText)
        if detect_words.isMeaningfulWords():
            # Задаем исходный регистр букв во взломанном шифротексте
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)

            # Спросить у поль зователя, найден ли ключ дешифрования
            print('Возможный взлом шифрования с помощью ключа %s:' % (possibleKey))
            print(decryptedText[:200])  # выводим первые 200 символов
            print()
            print('Введите D, если сделано, любой другой символ, чтобы продолжить взлом: ')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

    # Получить осмысленный текст не удалось , поэтому возвращаем None
    return None


def hackVigenere(ciphertext):
    # Прежде всего, необходимо применить метод Касиски
    # для выяснения возможной длины ключа
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    print(allLikelyKeyLengths)
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Результаты исследования Kasiski показывают, '
              'что наиболее вероятными длинами ключей являются: ' + keyLengthStr + '\n')
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Попытка взлома с длиной ключа %s (%s возможные ключи)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            break

    # Если ни один из найденных с помощью метода Касиски вариантов
    # длины ключа не сработал , начать атаку методом грубой силы
    if hackedMessage == None:
        if not SILENT_MODE:
            print('Не удалось взломать сообщение с вероятной длиной ключа. Перебор длины ключа...')
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # Не перепроверять длину ключа, уже опробованную методом Касиски
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print('Попытка взлома с длиной ключа %s (%s возможные ключи)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage != None:
                    break
    return hackedMessage


# If vigenereHacker.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()
