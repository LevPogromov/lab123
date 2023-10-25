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


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}! I can find determinant, rank, order and inv matrix.\n"
                         f"Example: \n"
                         f"Input:\n1 2 3\n4 5 6\n7 8 9\n\n"
                         f"Enter a your matrix NxN like in an example")


@dp.message(Command("det"))
async def command_return_determinant(message: types.Message):
    global matrix
    await message.answer(f"determinant matrix = {determinant(matrix)}")


@dp.message(Command("rank"))
async def command_return_rank(message: types.Message):
    global matrix
    await message.answer(f"rank matrix = {np.linalg.matrix_rank(matrix)}")


@dp.message(Command("order"))
async def command_return_order(message: types.Message):
    global matrix
    await message.answer(f"order matrix = {len(matrix)}")


@dp.message(Command("inv"))
async def command_return_inv(message: types.Message):
    global matrix
    def checkInvMatrix(matrix):
        if determinant(matrix)==0: return "Singular matrix"
        return np.linalg.inv(matrix)
    await message.answer(f"inv matrix = {checkInvMatrix(matrix)}")

@dp.message(Command("trans"))
async def command_return_transposedMatrix(message: types.Message):
    global matrix
    resMatrix = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            resMatrix += f"{matrix[j][i]} "
        resMatrix += "\n"
    await message.answer(f"transposed matrix = \n{resMatrix}")


@dp.message()
async def save_matrix(message: Message):
    newMessage = message.text.split()
    global matrix
    numbers = []
    for item in newMessage:
        try:
            item = int(item)
            numbers += [item]
        except ValueError:
            await message.answer("Uncorrect symbol!!!")
            return
    if len(numbers) ** 0.5 != int(len(numbers) ** 0.5):
        await message.answer("Error!!! Check Instruction!!!")
    else:
        n = int(len(numbers)**0.5)
        matrix = [numbers[i:i+n] for i in range(0, n*n, n)]
        await message.answer(f"Your matrix is saved.\n"
                             f"Choose what you want to do:\n"
                             f"/det\n"
                             f"/rank\n"
                             f"/inv\n"
                             f"/order\n"
                             f"/trans\n")


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())