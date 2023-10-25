import asyncio
import logging
import numpy as np
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import sys

TOKEN = "5764312410:AAFXT-B0oyzMV31nA5uGet-KmI3AIbkcx54"

dp = Dispatcher()


matrix = []
matrix2 = []

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}! How much matrix you have?\n"
                         f"/matrix1\n"
                         f"/matrix2")

@dp.message(Command("sum"))
async def sum_matrix(message: Message):
    global matrix, matrix2
    lent = len(matrix)
    sum_mat = ""
    for i in range(lent):
        for j in range(lent):
            sum_mat += f"{matrix[i][j]+matrix2[i][j]} "
        sum_mat += "\n"
    await message.answer(f"sum mat = \n{sum_mat}")



@dp.message(Command("matrix1"))
async def command_enter_matrix1(message: Message):
    await message.answer("Enter matrix NxN like an in example:\n"
                         "1 2 3\n"
                         "4 5 6\n"
                         "7 8 9\n")


@dp.message(Command("matrix2"))
async def command_enter_matrix2(message: Message):
    await message.answer("Enter matrixs NxN like an in example:\n"
                         "1 2 3\n"
                         "4 5 6\n"
                         "7 8 9\n"
                         "\n"
                         "1 2 3\n"
                         "4 5 6\n"
                         "7 8 9\n"
                         "You can use /sum\n/equat")

@dp.message(Command("equat"))
async def matrix_equation(message: Message):
    global matrix, matrix2
    await message.answer(f"if AX = B matrix product = \n{np.dot(np.linalg.inv(matrix), matrix2)}\n"
                         f"if XA = B matrix product = \n{np.dot(matrix2, np.linalg.inv(matrix))}")


@dp.message()
async def save_matrix(message: Message):
    global matrix
    global matrix2

    newMessage = message.text.split()
    numbers = []

    for item in newMessage:
        try:
            if item != "\n": numbers += [int(item)]
        except ValueError:
            await message.answer("Uncorrect symbol!!!")
            return

    if (len(numbers)/2) ** 0.5 == int((len(numbers)/2) ** 0.5):
        n = int((len(numbers)/2) ** 0.5)
        matrix = [numbers[i:i+n] for i in range(0, n*n, n)]
        matrix2 = [numbers[i:i+n] for i in range(n*n, 2*n*n, n)]

    elif len(numbers) ** 0.5 == int(len(numbers) ** 0.5):
        n = int(len(numbers) ** 0.5)
        matrix = [numbers[i:i + n] for i in range(0, n * n, n)]

    else:
        await message.answer("Error!!! Check Instruction!!!")



async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())