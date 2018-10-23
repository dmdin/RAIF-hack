import vkchatbot
from vk_api.bot_longpoll import VkBotMessageEvent
from vkchatbot.obj import MessageEvent, Message, Chat


class Update:
    def __init__(self, event, bot):
        """
        :type event: VkBotMessageEvent
        :type bot: vkchatbot.VkBot
        """
        self._event_raw = event

        self.chat_id = event.chat_id
        self.from_user = event.from_user
        self.from_chat = event.from_chat
        self.from_group = event.from_group

        self.obj = MessageEvent(event.obj)
        self.bot = bot

        if event.raw.get('action') is not None:
            self.action = True
            self.action_type = event.raw['action']['type']
            self.action_member_id = event.raw['action']['member_id']
        else:
            self.action = None
            self.action_raw = None

        self.user = bot.get_user(self.obj.from_id)
        if event.from_chat:
            self.chat = bot.get_chat(self.obj.peer_id)

            if self.chat is None:
                new_chat = Chat(self.obj.peer_id, self.obj.from_id, self.obj.date)
                bot.chats[new_chat.id] = new_chat
                self.chat = new_chat

        else:
            self.chat = None

        self.last_message_id = None  # type: int
        self.last_message = None  # type: Message


    def reply_text(self, text):
        """
        :type text: str
        """
        self.last_message = Message(text)
        self.last_message_id = self.bot.send_message(self.obj.peer_id, self.last_message)
        return self.last_message_id


    def reply(self, message):
        """
        :type message: Message
        """
        self.last_message = message
        self.last_message_id = self.bot.send_message(self.obj.peer_id, message)
        return self.last_message_id


    def edit_last_text(self, text, keep_forward=True, keep_snippets=True):
        if self.last_message_id is None:
            raise ValueError('You didnt send any messages via this update')
        self.last_message = Message(text)
        self.last_message_id = self.bot.edit_message(self.obj.peer_id, self.last_message_id,
                                                     self.last_message, keep_forward, keep_snippets)
        return self.last_message_id


    def edit_last(self, message, keep_forward=True, keep_snippets=True):
        if self.last_message_id is None:
            raise ValueError('You didnt send any messages via this update')
        self.last_message = message
        self.last_message_id = self.bot.edit_message(self.obj.peer_id, self.last_message_id,
                                                     message, keep_forward, keep_snippets)
        return self.last_message_id


    def upload_add(self, attach_type, filename=None,
                   from_url=None, doc_title=None, doc_tags=None):
        """
        :type attach_type: str
        :type filename: str
        :type from_url: str
        :type doc_title: str
        :type doc_tags: str
        """
        if self.last_message_id is None:
            raise ValueError('You didnt send any messages via this update')

        return self.bot.vk_attach_uploader.add(self.obj.peer_id, self.last_message_id,
                                               attach_type, filename, from_url, doc_title, doc_tags)


    def upload_start(self, message_final=None, one_by_one=False):
        """
        :type message_final: Message
        :type one_by_one: bool
        """
        if self.last_message_id is None or self.last_message is None:
            raise ValueError('You didnt send any messages via this update')

        return self.bot.vk_attach_uploader.start_uploading(self.last_message_id,
                                                           self.last_message, message_final, one_by_one)


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        s = '<Update>\n'
        if self.from_user:
            s += f'\tFrom {self.obj.from_id} user\n'
        elif self.from_chat:
            s += f'\tFrom {self.obj.from_id} chat {self.obj.peer_id}\n'
        else:
            # TODO if from group
            pass

        s += f'\tMessage: {self.obj.text}\n'
        s += f'\tAttachs: {",".join(self.obj.attachments) if len(self.obj.attachments) != 0 else "Nothing"}'

        return s
