from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def keyboard():
    button_1 = KeyboardButton(text="Добавить транзакцию")
    button_2 = KeyboardButton(text="Показать все транзакции")
    button_3 = KeyboardButton(text="Показать баланс")
    first_row = [button_1, button_2]
    second_row = [button_3]
    rows = [first_row, second_row]
    markup = ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)
    return markup


def purpose_keyboard():
    button_1 = KeyboardButton(text="Приход")
    button_2 = KeyboardButton(text="Уход")
    button_3 = KeyboardButton(text="Отмена")
    first_row = [button_1, button_2]
    second_row = [button_3]
    rows = [first_row, second_row]
    markup = ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)
    return markup
