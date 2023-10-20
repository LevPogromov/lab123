import asyncio
import logging
import numpy as np
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import sys

TOKEN = "5764312410:AAFXT-B0oyzMV31nA5uGet-KmI3AIbkcx54"

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}! I can find determinant, rank, order and inv matrix.\n"
                         f"Example: \n"
                         f"Input: 1 2 3\n4 5 6\n7 8 9\n Output: 0\n\n"
                         f"Enter a your matrix NxN like in an example")

@dp.message()
async def matrix_handler(message: types.Message):

    newMessage = message.text.split()
    numbers = [int(item) for item in newMessage]
    n = int(len(numbers) ** 0.5)
    matrix = [numbers[i:i + n] for i in range(0, n * n, n)]
    def determinant(matrix):

        if len(matrix) == 2 and len(matrix[0]) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        det = 0
        for c in range(len(matrix)):
            sub_matrix = [row[:c] + row[c + 1:] for row in matrix[1:]]
            # print(sub_matrix)
            sign = (-1) ** c
            det += sign * matrix[0][c] * determinant(sub_matrix)
        return det

    try:
        await message.answer(f"determinant = {determinant(matrix)}\n"
                             f"rank = {np.linalg.matrix_rank(matrix)}\n"
                             f"order matrix = {n}\n"
                             f"inv matrix = {np.linalg.inv(matrix)}")
    except TypeError:
        await message.answer("Check instruction")

async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())