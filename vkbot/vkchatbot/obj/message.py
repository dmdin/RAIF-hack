from typing import List, Tuple
from .keyboard import Keyboard


class Message:
    def __init__(self, text=None, attachments=None, forward_messages=None,
                 sticker_id=None, keyboard=None, remove_keyboard=False):
        """
        See https://vk.com/dev/messages.send for more info

        :param attachments: List of attachments, possible types:
                                - photo
                                - video
                                - audio
                                - doc
                                - wall
                                - market
                            Format: (type, owner_id, media_id, *access_key)
                                or: ('{type}{owner_id}_{media_id}{*"_"+access_key}'
                                        * - optional

        :type text: str
        :type attachments: List[Tuple[str]]
        :type forward_messages: List[int] or str
        :type sticker_id: int
        :type keyboard: Keyboard
        :type remove_keyboard: bool
        """

        self.text = text
        self.attachments = attachments
        self.forward_messages = forward_messages
        self.sticker_id = sticker_id
        if remove_keyboard:
            self.keyboard = Keyboard(one_time=True)
        else:
            self.keyboard = keyboard


    def copy(self):
        return self.__copy__()


    def __copy__(self):
        return Message(self.text,
                       self.attachments.copy(),
                       self.forward_messages.copy(),
                       self.sticker_id,
                       self.keyboard)
