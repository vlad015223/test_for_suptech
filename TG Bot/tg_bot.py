import logging
import pygsheets
from aiogram import Bot, Dispatcher, types, executor
from tokens import TG_TOKEN, SERVICE_FILE


logging.basicConfig(level=logging.ERROR, filename='TG BOT/errors.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

# в SERVICE_FILE записываем key_id сервисного аккаунта гугл (путь на json файл)
client = pygsheets.authorize(service_account_file=SERVICE_FILE)

# открываем нужную доку и лист
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
            # добавляем запись в первое пустое поле
            if value == '':
                worksheet.update_values(f"A{index+1}", [[user_login]])
                worksheet.update_values(f"B{index+1}", [[text]])
                worksheet.update_values(f"C{index+1}", [[formatted_date]])
                break
        
        # отправляем юзеру отбивку и ссылку на гуглдок
        await message.reply('Сообщение успешно записано!\nhttps://docs.google.com/spreadsheets/d/1gL-to78y5YGjDZMsHQ5w5hP4hC7D5kFZYmmY5BFqhdQ/edit#gid=0')

    # при появлении любой ошибки записываем её в файл errors.log
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    executor.start_polling(dp)
