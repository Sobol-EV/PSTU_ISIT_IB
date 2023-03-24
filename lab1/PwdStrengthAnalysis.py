

class PwdStrengthAnalysis:

    def __init__(self, password, s, m, v):
        self.password = password
        self.password_length = len(password)
        self.s = s
        self.m = m
        self.v = v
        self.n = self.__class__.__alphabet_power(password)
        self.pwd_space_power = self.n ** self.password_length
        print(f"M = {self.pwd_space_power}")

    __complexity_of_character_types = {
        'symbol': 33,
        'small': 26,
        'capital': 26,
        'number': 10
    }

    @staticmethod
    def __define_symbol(symbol):
        ascii_code = ord(symbol)
        if ((32 <= ascii_code) and (ascii_code <= 47)) or \
                ((58 <= ascii_code) and (ascii_code <= 64)) or \
                ((91 <= ascii_code) and (ascii_code <= 96)) or \
                ((123 <= ascii_code) and (ascii_code <= 126)):
            return True
        return False

    @staticmethod
    def __define_number(symbol):
        ascii_code = ord(symbol)
        if (48 <= ascii_code) and (ascii_code <= 57):
            return True
        return False

    @staticmethod
    def __define_capital_latin(symbol):
        ascii_code = ord(symbol)
        if (65 <= ascii_code) and (ascii_code <= 90):
            return True

        return False

    @staticmethod
    def __define_small_latin(symbol):
        ascii_code = ord(symbol)
        if (97 <= ascii_code) and (ascii_code <= 122):
            return True

        return False

    @classmethod
    def __alphabet_power(cls, password):
        alphabet = list(set(password))
        n = 0
        type_symbol = []
        for symbol in alphabet:
            if cls.__define_symbol(symbol):
                type_symbol.append('symbol')
            if cls.__define_number(symbol):
                type_symbol.append("number")
            if cls.__define_small_latin(symbol):
                type_symbol.append("capital")
            if cls.__define_capital_latin(symbol):
                type_symbol.append("small")
        type_symbol = list(set(type_symbol))
        for i in type_symbol:
            n += cls.__complexity_of_character_types[i]
        print(f"N = {n}")
        return n

    def __waiting_time_for_incorrect_input(self):
        result = (self.pwd_space_power // self.m) * self.v
        print(f"Время потраченное на ожидание:", result)
        return result

    @staticmethod
    def get_format_time(sec):
        t_dict = {
            "year": 31536000,
            "month": 2592000,
            "days": 86400,
            "hours": 3600,
            "minuts": 60
        }

        for key in t_dict:
            temp = t_dict[key]
            t_dict[key] = sec // temp
            sec -= t_dict[key] * temp

        print(
            f"ИТОГ: "
            f"{t_dict['year']} л. {t_dict['month']} мес. "
            f"{t_dict['days']} д. {t_dict['hours']} ч. "
            f"{t_dict['minuts']} мин. {sec} сек."
        )

    def analyze_the_password(self):
        print(self.pwd_space_power, " ", self.s)
        t = self.pwd_space_power / self.s
        print(f"Время активного перебора пароля: {t} сек.")
        result_sec = self.__waiting_time_for_incorrect_input() + t
        if t % 2 == 0:
            result_sec -= self.v
        print("Общее время перебора (с учётом ожиданий): ", result_sec)
        return result_sec
