import os
import time
import random
import tempfile
import requests
import threading
import vkchatbot
from typing import Dict, List
from vkchatbot.obj import Message


class VkAttachUploader:
    def __init__(self, bot):
        """
        :type bot: vkchatbot.VkBot
        """
        self.bot = bot
        self.queues = {}  # type: Dict[int, List[tuple]]
        self.tmp_path = tempfile.gettempdir()


    def add(self, peer_id, message_id, attach_type, filename=None,
            from_url=None, doc_title=None, doc_tags=None):
        """
        :type peer_id: int
        :type message_id: int
        :type attach_type: str
        :type filename: str
        :type from_url: str
        :type doc_title: str
        :type doc_tags: str
        """
        if filename is not None and from_url is not None:
            raise ValueError('You must specify only one argument: filename or from_url')

        if self.queues.get(message_id) is None:
            self.queues[message_id] = []

        self.queues[message_id].append((peer_id, attach_type, filename, from_url, doc_title, doc_tags))


    def start_uploading(self, message_id, message_to_edit, message_final=None, one_by_one=False):
        """
        :type message_id: int
        :type message_to_edit: Message
        :type message_final: Message
        :type one_by_one: bool
        """
        if len(self.queues[message_id]) == 0:
            return

        peer_id = 0
        attachs_all = self.queues.pop(message_id)
        for attach_element in attachs_all:
            upload_thread = threading.Thread(target=self._upload_thread,
                                             args=(attach_element, message_id,
                                                   message_to_edit, message_final, one_by_one))
            upload_thread.start()

        if not one_by_one:
            self.bot.edit_message(peer_id, message_id, message_final)
        # print(f'Uploading completed {time.clock():.2f}')


    def _upload_thread(self, attach_element, message_id, message_to_edit, message_final, one_by_one):
        """
        :type attach_element: tuple
        :type message_id: int
        :type message_to_edit: Message
        :type message_final: Message
        :type one_by_one: bool
        """

        peer_id, attach_type, filename, from_url, doc_title, doc_tags = attach_element
        if from_url is not None:
            random_name = ''
            file_extension = from_url.split('.')[-1]
            while random_name == '' or random_name in os.listdir(self.tmp_path):
                random_name = f'vkattach-{peer_id}-{message_id}-{random.randint(10**6, 10**7-1)}.{file_extension}'
            random_name = f'{self.tmp_path}/{random_name}'
            rawfile = requests.get(from_url).content
            with open(random_name, 'wb') as tmpfile:
                tmpfile.write(rawfile)

            filename = random_name
        else:
            random_name = None

        if attach_type == 'photo':
            photo = self.bot.vk_upload.photo_messages(filename)[0]  # type: dict
            owner_id = -self.bot.id
            attach_id = photo['id']
        elif attach_type == 'doc':
            if doc_title is None:
                doc_title = 'Document'
            if doc_tags is None:
                doc_tags = 'Tags'

            doc = self.bot.vk_upload.document_message(filename, doc_title, doc_tags, peer_id)[0]  # type: dict
            owner_id = peer_id
            attach_id = doc['id']
        else:
            # TODO other attachments
            raise ValueError(f'Unknown attach_type "{attach_type}"')

        if random_name is not None:
            os.remove(random_name)

        new_attach = (attach_type, owner_id, attach_id)

        if message_final is None:
            message_final = message_to_edit.copy()

        if message_final.attachments is None:
            message_final.attachments = [new_attach]
        else:
            message_final.attachments.append(new_attach)

        # print(f'Attach {doc_title} ready {time.clock():.2f}')
        if one_by_one:
            self.bot.edit_message(peer_id, message_id, message_final)
            # print(f'Attach {doc_title} completed {time.clock():.2f}')
