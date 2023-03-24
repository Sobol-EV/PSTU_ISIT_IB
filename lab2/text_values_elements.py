#  Названия окон
NAME_WINDOW_AUTH = "Авторизация"
NAME_WINDOW_ERROR_BAN = "OPS... It's BAN!"
NAME_WINDOW_ERROR_AUTH = "Неудачно!"
NAME_WINDOW_ERROR_UPDATE_PASSWORD = "Неверный пароль!"
NAME_WINDOW_SUCCESSFULLY_PASSWORD = "Успешно!"
NAME_WINDOW_UPDATE_PASSWORD = "Изменить пароль"
NAME_WINDOW_PERSONAL_AREA = u"Личный кабинет"
NAME_WINDOW_ERROR_UPDATE_DATA = "Данные не корректны!"
NAME_WINDOW_ERROR_DELETE_USER = "Ошибка при удалении!"

#  Названия кнопок
BUTTON_AUTH = "Авторизироваться"
BUTTON_CONFIRM_UPDATE_PASSWORD = u"Подтвердить "
BUTTON_UPDATE_PASSWORD = u"Изменить пароль"
BUTTON_EXIT_PERSONAL_AREA = u"Выйти"
BUTTON_ADD_USER = u"Добавить пользователя"
BUTTON_DELETE_USER = u"Удалить пользователя"
BUTTON_UPDATE_USER = u"Обновить данные"
BUTTON_SAVE_UPDATE = u"Записать изменения"

# Текст интерфейса
TEXT_LOGIN_AUTH = "Логин: "
TEXT_PASSWORD_AUTH = "Пароль:     "
TEXT_OLD_PASSWORD = u"Введите старый пароль: "
TEXT_NEW_PASSWORD = u"Введите новый пароль:"
TEXT_CONFIRM_NEW_PASSWORD = u"Повторите новый пароль:"
TEXT_LOGIN_PERSONAL_AREA = u"Логин: "
TEXT_RIGHTS_PERSONAL_AREA = u"Тип прав: "
TEXT_RIGHTS_USER = "Пользователь"
TEXT_RIGHTS_ADMIN = "Админ"


#  Текст сообщений
MSG_BLOCK_USER = "Вы заблокированы! \nОбратитесь к администратору!"
MSG_FAILED_PASSWORD_RULES = f"Пароль не соответствует требованиям безопасности!\n " \
                            f"Требования написаны под кнопкой <Подтвердить>."
MSG_FAILED_PASSWORD_CONFIRM = f"Пароли не совпадают, проверьте правильность\nвведёных данных."
MSG_FAILED_OLD_PASSWORD = f"Старый пароль введён некорректно,\n проверьте правильность указанных данных."
MSG_SUCCESSFULLY_PASSWORD = f"Пароль успешно изменён!\nАвторизируйтесь с помощью нового пароля."
MSG_NO_RULES_PASSWORD = "Пароль может быть любого формата т.к правило не задано."
MSG_NO_TEXT_RULES_PASSWORD = "Администратор не описал правило,\n но задал шаблон для проверки!" \
                             "\nОбратитесь за помощью к ему."
MSG_EMPTY_FIELD = "Столбцы 2, 4, 5, 6, 7 - не должны быть пустыми!"
MSG_NON_UNIQUE_LOGIN = "Логин должен быть уникальным!"
MSG_NO_SELECT_ROW = "Не выбран ни один пользователь!"
MSG_NO_DELETE_SELF = "Нельзя удалить себя!"


def error_auth(count_error):
    return f"Неверный логин или пароль!\n " \
           f"Осталось попыток: {count_error}"
