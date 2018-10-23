import time
from typing import Dict
from vk_api.vk_api import VkApiMethod
from vk_api import VkUpload
from vkchatbot.ext import VkAttachUploader
from vkchatbot.obj import User, Chat, Message


class VkBot:
    def __init__(self, group_id, vk_api, vk_upload):
        """
        :type group_id: int
        :type vk_api: VkApiMethod
        :type vk_upload: VkUpload
        """
        self.id = group_id

        self.vk_api = vk_api
        self.vk_upload = vk_upload
        self.vk_attach_uploader = VkAttachUploader(self)

        self.users = {}  # type: Dict[int, User]
        self.chats = {}  # type: Dict[int, Chat]

        self.statistics = {'self_msg_recieve': 0,
                           'chat_msg_recieve': 0,
                           'self_msg_send':    0,
                           'chat_msg_send':    0,
                           'active_users':     0,
                           'active_chats':     0,
                           'time_initiated':   0}

        self.config = {'user_autoclear':      True,
                       'send_stickers_first': True}


    def on_init(self):
        self.statistics['time_initiated'] = int(time.time())


    def get_user(self, user_id) -> User:
        """
        :type user_id: int
        """
        user = self.users.get(user_id)
        if user is None:
            user = User(user_id, self.config['user_autoclear'])
            self.users[user_id] = user
        return user


    def get_chat(self, chat_id) -> Chat:
        """
        :type chat_id: int
        """
        chat = self.chats.get(chat_id)
        return chat


    def send_message(self, to_id, message):
        """
        :type to_id: int
        :type message: Message or str
        """

        if isinstance(message, Message):
            send_params = self.get_send_params(message)
            sticker = message.sticker_id

            if sticker is not None and self.config['send_stickers_first']:
                self.vk_api.messages.send(peer_id=to_id, sticker_id=sticker)
                sticker = None

            resp = self.vk_api.messages.send(peer_id=to_id, **send_params)

            if sticker is not None:
                self.vk_api.messages.send(peer_id=to_id, sticker_id=message.sticker_id)

            return resp
        elif isinstance(message, str):
            resp = self.vk_api.messages.send(peer_id=to_id, message=message)
            return resp
        else:
            raise ValueError('Message must be a str or vkchatbot.obj.Message type')


    def edit_message(self, peer_id, message_id, message, keep_forward_messages=True, keep_snippets=True):
        """
        :type peer_id: int
        :type message_id: int
        :type message: Message or str
        :type keep_forward_messages: bool
        :type keep_snippets: bool
        """

        if isinstance(message, Message):
            if message.sticker_id is not None:
                raise ValueError('Cant edit message with sticker')
            send_params = self.get_send_params(message)
        elif isinstance(message, str):
            send_params = dict()
            send_params['message'] = message
        else:
            raise ValueError('Message must be a str or vkchatbot.obj.Message type')

        send_params['keep_forward_messages'] = '1' if keep_forward_messages else '0'
        send_params['keep_snippets'] = '1' if keep_snippets else '0'

        resp = self.vk_api.messages.edit(peer_id=peer_id, message_id=message_id, **send_params)
        return resp


    def get_send_params(self, message) -> Dict[str, str]:
        """
        :type message: Message
        """
        send_params = {}
        if message.text is not None:
            send_params['message'] = message.text

        if message.attachments is not None:
            send_params['attachment'] = []
            for attach in message.attachments:
                if isinstance(attach, tuple):
                    att_type, att_owner_id, att_id = attach[:3]
                    if len(attach) == 4:
                        att_key = '_' + attach[3]
                    else:
                        att_key = ''

                    attach_str = f'{att_type}{att_owner_id}_{att_id}{att_key}'
                else:
                    attach_str = attach
                send_params['attachment'].append(attach_str)

            send_params['attachment'] = ','.join(send_params['attachment'])
        if message.forward_messages is not None:
            if isinstance(message.forward_messages, list):
                send_params['forward_messages'] = ','.join(map(str, message.forward_messages))
            elif isinstance(message.forward_messages, str):
                send_params['forward_messages'] = message.forward_messages

        if message.keyboard is not None:
            send_params['keyboard'] = message.keyboard.get_keyboard()

        return send_params
