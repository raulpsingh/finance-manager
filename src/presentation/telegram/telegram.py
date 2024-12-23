import asyncio
from threading import Thread
from aiogram import Bot, Dispatcher
from src.presentation.telegram.telegram_handlers import router


class TelegramBot:
    def __init__(self, api_token):
        self.bot = Bot(token=api_token)
        self.dp = Dispatcher()
        self.loop = None
        self.thread = None

    def start(self):
        """Запуск бота в отдельном потоке."""
        if self.thread and self.thread.is_alive():
            print("Бот уже запущен.")
            return

        def _run():
            self.loop = asyncio.new_event_loop()  # Создаём новый цикл событий
            asyncio.set_event_loop(self.loop)
            try:
                self.loop.run_until_complete(self.execute())  # Запускаем выполнение
            except asyncio.CancelledError:
                pass
            finally:
                self.loop.close()

        self.thread = Thread(target=_run, daemon=True)
        self.thread.start()
        print("Telegram-бот запущен.")

    async def execute(self):
        """Основной метод для запуска бота."""
        self.dp.include_routers(router)
        await self._polling()

    async def _polling(self):
        """Запуск поллинга."""
        await self.dp.start_polling(self.bot, skip_updates=True)

    def stop(self):
        """Остановка бота."""
        if not self.loop:
            print("Бот не запущен.")
            return

        async def _stop():
            await self.dp.stop_polling()
            await self.bot.session.close()
            print("Бот успешно остановлен.")

        # Безопасно вызываем остановку бота в его цикле событий
        asyncio.run_coroutine_threadsafe(_stop(), self.loop)
        self.thread.join()  # Ждём завершения потока
        print("Поток бота завершён.")
