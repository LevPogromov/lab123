import asyncio
import logging
import numpy as np
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import sys

TOKEN = token

dp = Dispatcher()
matrix = []
matrix2 = []

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
    await message.answer(f"Hello, {message.from_user.full_name}! How much matrix you have?\n"
                         f"Для работы с одной матрицей - /matrix1\n"
                         f"Для работы с двумя матрицами - /matrix2")


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
                         "7 8 9\n")




#func for 1 matrix
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


#func for 2 matrix
@dp.message(Command("sum"))
async def sum_matrix(message: Message):
    global matrix, matrix2
    lent = len(matrix)
    sum_mat = ""
    for i in range(lent):
        for j in range(lent):
            sum_mat += f"{matrix[i][j]+matrix2[i][j]} "
        sum_mat += "\n"
    await message.answer(f"sum matrix = \n{sum_mat}")


@dp.message(Command("prod"))
async def matrix_product(message: Message):
    global matrix, matrix2
    await message.answer(f"matrix product = \n{np.dot(matrix, matrix2)}\n")


@dp.message(Command("equat"))
async def matrix_equation(message: Message):
    global matrix, matrix2
    def checkInvMatrix(matrix):
        if determinant(matrix)==0: return "Singular matrix"
        return np.linalg.inv(matrix)
    invMatrix = checkInvMatrix(matrix)
    if (type(invMatrix) != "str"):
        await message.answer(f"if AX = B matrix product = \n{np.dot(invMatrix, matrix2)}\n\n"
                             f"if XA = B matrix product = \n{np.dot(matrix2, invMatrix)}")
    else:
        await message.answer(f"first matrix is Singular matrix")

#save matrix
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
        await message.answer("Two matrix are saved.\n"
                             "Choose what you want to do:\n"
                             "Матричное уравнение - /equat\n"
                             "Сумма матриц - /sum\n"
                             "Произведение матриц - /prod\n")

    elif len(numbers) ** 0.5 == int(len(numbers) ** 0.5):
        n = int(len(numbers) ** 0.5)
        matrix = [numbers[i:i + n] for i in range(0, n * n, n)]
        await message.answer(f"Your matrix is saved.\n"
                             f"Choose what you want to do:\n"
                             f"Детерминант - /det\n"
                             f"Ранг матрицы - /rank\n"
                             f"Обратная матрица - /inv\n"
                             f"Порядок /order\n"
                             f"Транспонированная матрица - /trans\n")
    else:
        await message.answer("Error!!! Check Instruction!!!")



async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
