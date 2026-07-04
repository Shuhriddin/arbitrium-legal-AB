from aiogram.filters import Filter
from aiogram import types

class NumericFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        text = getattr(message, 'text', '')
        return isinstance(text, str) and text.isdigit()