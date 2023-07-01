import logging
import pygsheets
from aiogram import Bot, Dispatcher, types, executor
from tokens import TG_TOKEN, SERVICE_FILE

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

client = pygsheets.authorize(service_account_file=SERVICE_FILE)

spreadsheet = client.open("test_for_suptech")
worksheet = spreadsheet.worksheet_by_title("Лист1")

@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        user_login = message.from_user.username
        text = message.text
        message_date = message.date
        formatted_date = message_date.strftime("%Y-%m-%d %H:%M:%S")

        last_row = worksheet.get_col(1)
        for index, value in enumerate(last_row):
            if value == '':
                # добавляем запись в первое пустое поле
                worksheet.update_values(f"A{index+1}", [[user_login]])
                worksheet.update_values(f"B{index+1}", [[text]])
                worksheet.update_values(f"C{index+1}", [[formatted_date]])
                break

        await message.reply('Сообщение успешно записано!\nhttps://docs.google.com/spreadsheets/d/1gL-to78y5YGjDZMsHQ5w5hP4hC7D5kFZYmmY5BFqhdQ/edit#gid=0')

    except Exception as e:
        logging.exception(e)
        with open('errors.log', 'a') as f:
            f.write(f'Time: {message.date}, Error: {str(e)}\n')

if __name__ == '__main__':
    executor.start_polling(dp)