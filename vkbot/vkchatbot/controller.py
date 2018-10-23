import time
import queue
import vk_api
import threading
import traceback
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from .bot import VkBot
from .update import Update
from vkchatbot.obj import CarefulThread
from vkchatbot.obj.handlers import handlers, pacifier, error_pacifier
from vkchatbot.ext import ConversationHandler


class Controller:
    def __init__(self, group_id, access_token):
        """
        :type group_id: int
        :type access_token: str
        """
        self.group_id = group_id
        self.access_token = access_token

        self.vk_session = vk_api.VkApi(token=access_token)

        self.vk_longpoll = VkBotLongPoll(self.vk_session, self.group_id)
        self.vk_uploader = VkUpload(self.vk_session)

        self.bot = VkBot(group_id, self.vk_session.get_api(), self.vk_uploader)

        self.handlers = handlers
        self.error_handler = error_pacifier


    def run(self):
        print('<< Bot initialized >>'.center(50))

        threads_bucket = queue.Queue()
        exc_thread = threading.Thread(target=Controller.exceptions_checker,
                                      name='Exception checker',
                                      args=(self, threads_bucket,))
        exc_thread.start()

        for event in self.vk_longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_EDIT:
                if int(event.obj.from_id) == -self.group_id:
                    continue

            if event.type in [VkBotEventType.MESSAGE_NEW, VkBotEventType.MESSAGE_EDIT]:
                update = Update(event, self.bot)

                user = update.user
                chat = update.chat

                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.from_user:
                        self.bot.statistics['self_msg_recieve'] += 1
                        user.on_new_message(in_chat=False)
                    elif event.from_chat:
                        self.bot.statistics['chat_msg_recieve'] += 1
                        user.on_new_message(in_chat=True)
                        chat.on_new_message()

                if self.handlers[VkBotEventType.MESSAGE_NEW] is not None:
                    convh = self.handlers[VkBotEventType.MESSAGE_NEW]  # type: ConversationHandler
                    callback = convh.get_callback(user)
                    thread = CarefulThread(threads_bucket, update, target=callback, args=(update,))
                    thread.start()

            else:
                self.handlers[event.type](event)


    def exceptions_checker(self, threads_bucket):
        """
        :type threads_bucket: queue.Queue
        """
        while True:
            try:
                exc, old_update = threads_bucket.get()
                self.error_handler(old_update, exc)
            except queue.Empty:
                print('Nothing in queue')
            except Exception:
                print('Error in error handler :(')
                print(traceback.print_exc())
            finally:
                time.sleep(3)
