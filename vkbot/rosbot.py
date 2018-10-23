import os
import time
import json
import random
import requests
import traceback
from pprint import pprint
from vk_api.bot_longpoll import VkBotEventType
from vkchatbot import Controller, Update, VkBot
from vkchatbot.obj import Message, Keyboard, VkKeyboardColor
from vkchatbot.ext import ConversationHandler


class ExampleBot:
    def __init__(self, admin_id):
        self.data = {}
        self.admin_id = admin_id

    def entry(self, update: Update):
        update.reply_text('Добрый день! Я могу подсчитать кадастровую стоимость объекта по некоторым параметрам\n'
                          'Я спрошу у вас разные параметры вашего объекта, для '
                          'которого вы хотите узнать кадастровую стоимость, '
                          'а после выдам отчет.')
        update.obj.text = ''
        update.user.change_page('main')
        return self.main(update)

    def main(self, update: Update):
        if update.obj.text.lower() == 'начать':
            update.user.change_page('inp_area')
            update.obj.text = ''
            return self.input_area(update)
        else:
            update.reply(Message('Напишите мне "Начать", чтобы запустить Rosreestr AI\n',
                                 keyboard=Keyboard(('Начать', VkKeyboardColor.PRIMARY), one_time=True)))

    def input_area(self, update: Update):
        if update.obj.text == '':
            update.reply_text('Введите площадь помещения')
            update.user.change_page('area')
        else:
            update.user.data['area'] = update.obj.text
            update.obj.text = ''
            return self.input_floors(update)

    def input_floors(self, update: Update):
        if update.obj.text == '':
            update.reply_text('Введите количество этажей в здании')
            update.user.change_page('floors')
        else:
            update.user.data['floors'] = update.obj.text
            update.obj.text = ''
            return self.input_year(update)

    def input_year(self, update: Update):
        if update.obj.text == '':
            update.reply_text('Введите год постройки здания')
            update.user.change_page('year')
        else:
            update.user.data['year'] = update.obj.text
            update.obj.text = ''
            return self.input_wallm(update)

    def input_wallm(self, update: Update):
        if update.obj.text == '':
            update.reply_text('Введите материал стен здания')
            update.user.change_page('wallm')
        else:
            update.user.data['wallm'] = update.obj.text
            update.obj.text = ''
            return self.inp_kladr(update)

    def inp_kladr(self, update: Update):
        if update.obj.text == '':
            update.reply_text('Введите код КЛАДР здания')
            update.user.change_page('kladr')
        else:
            update.user.data['kladr'] = update.obj.text
            update.obj.text = ''
            return self.inp_center(update)

    def inp_center(self, update: Update):
        if update.obj.text == '':
            update.reply_text('Введите расстояние до центра города (в метрах)')
            update.user.change_page('center')
        else:
            update.user.data['center'] = update.obj.text
            update.obj.text = ''
            return self.inp_transport(update)

    def inp_transport(self, update: Update):
        if update.obj.text == '':
            update.reply_text('Введите расстояние до ближайшей остановки общественного транспорта (в метрах)')
            update.user.change_page('transport')
        else:
            update.user.data['transport'] = update.obj.text
            update.obj.text = ''
            return self.predict(update)

    def predict(self, update: Update):
        if update.obj.text == '':
            update.reply_text('Отлично! Все данные введены, подготавливаю отчет...')
            update.reply_text(str(update.user.data))
            update.user.change_page('main')

    def on_errors(self, update: Update, exc):
        strsxc = traceback.format_exception(*exc)
        del strsxc[1:2]
        print('Error!\n', *strsxc)
        update.reply_text('Sorry, some error occured')
        # admin_msg = Message(text=f'Error!\n{str(update)}\n=== Traceback info ===\n{"".join(strsxc)}')
        # update.bot.send_message(self.admin_id, admin_msg)


if __name__ == '__main__':
    """
    config.json ->
        {
            "group_id": Your group id,
            "access_token": Group access token,
            "admin_id": Your VK id (bot can send you exceptions)
        }
    """
    with open('config.json') as file:
        config = json.load(file)
        group_id = config['group_id']
        access_token = config['access_token']
        admin_id = config['admin_id']

    bot_controller = Controller(group_id, access_token)

    RosreestrBot = ExampleBot(admin_id=admin_id)

    ch = ConversationHandler(entry_callback=RosreestrBot.entry, pages={
        'main':      RosreestrBot.main,
        'area':      RosreestrBot.input_area,
        'floors':    RosreestrBot.input_floors,
        'year':      RosreestrBot.input_year,
        'wallm':     RosreestrBot.input_wallm,
        'kladr':     RosreestrBot.inp_kladr,
        'center':    RosreestrBot.inp_center,
        'transport': RosreestrBot.inp_transport
        })

    bot_controller.handlers[VkBotEventType.MESSAGE_NEW] = ch
    bot_controller.error_handler = RosreestrBot.on_errors

    bot_controller.run()
