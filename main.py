import asyncio
import os

from dotenv import load_dotenv

from src.application.use_cases.add_transaction import AddTransactionUseCase
from src.application.use_cases.get_all_transactions import GetAllTransactionsUseCase
from src.application.use_cases.get_balance import GetBalanceUseCase
from src.infrastructure.repositories.json_manager_repository import JsonManagerRepository
from src.infrastructure.repositories.sql_manager_repository import SqlManagerRepository
from src.presentation.cli.menu import Cli
from src.presentation.telegram.telegram import TelegramBot

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


async def main():
    repo = JsonManagerRepository(".data/transactions.json")
    repo2 = SqlManagerRepository(".data/transactions.db")
    add_transaction_use_case = AddTransactionUseCase(repo2)
    get_all_transactions_use_case = GetAllTransactionsUseCase(repo2)
    get_balance_use_case = GetBalanceUseCase(repo2)
    telegram_bot = TelegramBot(API_TOKEN)

    actions = {
        '1': lambda: Cli.add_transaction(add_transaction_use_case),
        '2': lambda: Cli.get_all_transactions(get_all_transactions_use_case),
        '3': lambda: Cli.get_balance(get_balance_use_case),
        "4": lambda: Cli.start_bot(telegram_bot),
        "5": lambda: asyncio.create_task(Cli.stop_bot(telegram_bot))

    }

    await Cli.display_menu(actions)


if __name__ == '__main__':
    asyncio.run(main())
