from PwdStrengthAnalysis import PwdStrengthAnalysis


if __name__ == "__main__":
    pwd = input("Введите пароль: ")
    s = float(input("Введите скорость перебора паролей в секунду (s): "))
    m = float(input("Введите количество неправильных попыток (m): "))
    v = float(input("Введите время паузы в секундах (v): "))
    a = PwdStrengthAnalysis(pwd, s, m, v)
    a.get_format_time(a.analyze_the_password())
