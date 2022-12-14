import logging
from aiogram import Bot,types,Dispatcher,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from db import *
from config import *
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())
db=Database("database.db")
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(mess:types.Message):
    await mess.answer("Qaysi futbolchi haqida ma'lumot olishni xohlaysiz?")

@dp.message_handler(commands="menu")
async def menu(mess:types.Message):
    await mess.answer("Quyidagilardan tanlang",reply_markup=markup)

@dp.callback_query_handler(text="insert",state=None)
async def insert(call:types.CallbackQuery):
    await call.answer()
    await call.message.answer("Futbolchining ismini kiriting")
    await Kiritish.ismi.set()

@dp.callback_query_handler(text="delete")
async def delete(call:types.CallbackQuery):
    await call.answer()
    db.delete_players()
    await call.message.answer("Barcha futbolchilar o'chirildi")

@dp.callback_query_handler(text = "search")
async def search(call:types.CallbackQuery):
    await call.answer()
    await call.message.answer("Futbolchi ismini yozib yuboring")

@dp.message_handler(state=Kiritish.ismi)
async def isminikiritish(mess:types.Message,state:FSMContext):

    await state.update_data({"ismi":mess.text})
    await Kiritish.next()
    await mess.answer("Futbolchining telefon raqamini kiriting")

@dp.message_handler(state=Kiritish.telefon_raqam)
async def raqamkiritish(mess:types.Message,state:FSMContext):

    if len(mess.text)==12:
        await state.update_data({"telefon_raqam":mess.text})
        await mess.answer("Futbolchi raqamini kiriting")
        await Kiritish.next()

    else:
        await mess.answer("Telefon raqam noto'g'ri formatda kiritildi")

@dp.message_handler(state=Kiritish.raqami)
async def raqamkiritsh(mess:types.Message,state:FSMContext):
    if mess.text.isdigit() and float(mess.text)<11.0 and float(mess.text)>0.0:
        await state.update_data({"raqami":mess.text})
        await Kiritish.next()
        await mess.answer("Futbolchining jamoasini kiriting")
    else:
        await mess.answer("Bu futbolchining raqami bo'la olmaydi")

@dp.message_handler(state=Kiritish.jamoa)
async def jamoakiritish(mess:types.Message,state:FSMContext):
    await state.update_data({"jamoa": mess.text})
    data = await state.get_data()
    if db.player_exists(ismi=data['ismi'],telefon_raqam=data['telefon_raqam'],raqami=data['raqami'],jamoa=data['jamoa']):
        await mess.answer("Bu futbolchi avval ham kiritilgan")
        await state.finish()
    else:
        db.futbolchi_kiritish(ismi=data['ismi'],telefon_raqam=data['telefon_raqam'],raqami=data['raqami'],jamoa=data['jamoa'])
        await mess.answer("Muvaffaqiyatli qo'shildi")
        await state.finish()

@dp.message_handler()
async def main(mess:types.Message):
    result =  db.get_player(ismi = mess.text)
    await mess.answer(result)

if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)