from typing import Optional
from threading import Thread

from src.application.dto.transaction_dto import TransactionDTO
from src.domain.value_objects.category import Category
from src.domain.value_objects.purpose import Purpose
from src.presentation.cli.messages import MESSAGES
from src.presentation.telegram.telegram import TelegramBot


class Cli:
    @staticmethod
    async def display_menu(actions) -> None:
        while True:
            print(MESSAGES['menu'])
            choice = input("\nВыберите действие: ")

            if choice in actions:
                await actions[choice]()
            elif choice == '6':
                print("Выход")
            else:
                print("Неверный ввод")

    @staticmethod
    def get_transaction_details(purpose: Purpose) -> tuple[str, Optional[str]]:
        amount = input("Введите сумму: ")
        category = None

        if purpose.value == "OUTCOME":
            categories = MESSAGES["categories"]
            print("\nДоступные категории:")
            print("\n".join(f"{num}. {label}" for num, (label, _) in enumerate(categories.items(), start=1)))
            # type: ignore
            while True:
                choice = input("\nВыберите категорию (введите номер): ")
                if choice.isdigit() and 1 <= int(choice) <= len(categories):
                    category = list(categories.values())[int(choice) - 1]  # type: ignore
                    break
                else:
                    print("Некорректный выбор. Попробуйте снова.")

        return amount, category

    @staticmethod
    def _get_purpose() -> Optional[Purpose]:
        print(MESSAGES['transaction_type'])
        choice = input("\nВаш выбор: ")

        if choice == "1":
            return Purpose("INCOME")
        elif choice == "2":
            return Purpose("OUTCOME")
        elif choice == "3":
            return None
        else:
            print("Некорректный ввод")
            return None

    @staticmethod
    async def add_transaction(use_case):
        while True:
            purpose = Cli._get_purpose()
            if not purpose:
                break

            amount, category = Cli.get_transaction_details(purpose)
            try:
                use_case.execute(amount=amount, purpose=purpose, category=Category(category))
            except ValueError as e:
                print(e)

    @staticmethod
    async def get_all_transactions(use_case):
        transactions = use_case.execute()
        for transaction in transactions:
            print(TransactionDTO.from_transaction(transaction))

    @staticmethod
    async def get_balance(use_case):
        balance = use_case.execute()
        print(balance)

    @staticmethod
    async def start_bot(telegram_bot: TelegramBot):
        telegram_bot.start()
        print("Telegram-бот работает в фоновом режиме.")

    @staticmethod
    async def stop_bot(telegram_bot: TelegramBot):
        telegram_bot.stop()
