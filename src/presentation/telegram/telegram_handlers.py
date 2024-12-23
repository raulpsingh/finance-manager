from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.application.dto.transaction_dto import TransactionDTO
from src.application.use_cases.add_transaction import AddTransactionUseCase
from src.application.use_cases.get_all_transactions import GetAllTransactionsUseCase
from src.application.use_cases.get_balance import GetBalanceUseCase
from src.domain.value_objects.category import Category
from src.domain.value_objects.purpose import Purpose
from src.infrastructure.repositories.sql_manager_repository import SqlManagerRepository
from src.presentation.telegram import keyboards
from src.presentation.telegram.states import CurrentStates
from src.presentation.telegram.utils import CATEGORIES

router = Router()

repo2 = SqlManagerRepository(".data/transactions.db")
add_transaction_use_case = AddTransactionUseCase(repo2)
get_all_transactions_use_case = GetAllTransactionsUseCase(repo2)
get_balance_use_case = GetBalanceUseCase(repo2)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(CurrentStates.waiting_for_click)
    await message.answer(text="Привет, это приложение для управления финансами", reply_markup=keyboards.keyboard())


@router.message(F.text == "Добавить транзакцию")
async def add_transaction_button(message: Message, state: FSMContext):
    await state.set_state(CurrentStates.waiting_for_purpose)
    await message.answer(text="Пожалуйста выберите тип транзакции:", reply_markup=keyboards.purpose_keyboard())


@router.message(F.text == "Показать все транзакции")
async def get_all_transactions_button(message: Message, state: FSMContext):
    result = get_all_transactions_use_case.execute()
    for transaction in result:
        await message.answer(str(TransactionDTO.from_transaction(transaction)))


@router.message(F.text == "Показать баланс")
async def get_balance_button(message: Message, state: FSMContext):
    result = get_balance_use_case.execute()
    await message.answer(str(result))


@router.message(CurrentStates.waiting_for_purpose)
async def purpose_buttons(message: Message, state: FSMContext):
    if message.text in ["Приход", "Уход"]:
        await state.update_data(transaction_type=message.text)
        await message.answer("Введите сумму:")
        await state.set_state(CurrentStates.waiting_for_sum)
    elif message.text == "Отмена":
        await message.answer("Отмена", reply_markup=keyboards.keyboard())
        await state.set_state(CurrentStates.waiting_for_click)
    else:
        await message.answer("Неверный ввод")


@router.message(CurrentStates.waiting_for_sum)
async def sum_input(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("Введите корректную сумму.")
        return

    data = await state.get_data()
    if data['transaction_type'] == "Приход":
        add_transaction_use_case.execute(amount=message.text, purpose=Purpose("INCOME")
                                         , category=Category(None))
    elif data['transaction_type'] == "Уход":
        await state.update_data(amount=message.text)
        await message.answer("Выберите категорию:", reply_markup=keyboards.category_keyboard())
        await state.set_state(CurrentStates.waiting_for_category)


@router.message(CurrentStates.waiting_for_category)
async def process_category(message: Message, state: FSMContext):
    category = message.text.lower().strip()
    data = await state.get_data()  # Получаем все данные
    try:
        if category.lower() in CATEGORIES:
            add_transaction_use_case.execute(amount=data['amount'], purpose=Purpose("OUTCOME")
                                             , category=CATEGORIES[category])
        else:
            raise ValueError("Неверная категория")
    except ValueError as e:
        await message.answer(str(e), reply_markup=keyboards.keyboard())

    await message.answer(f"Транзакция сохранена", reply_markup=keyboards.keyboard())
    await state.set_state(CurrentStates.waiting_for_click)  # Сбрасываем состояние
