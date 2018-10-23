from typing import List, Dict


class User:
    def __init__(self, user_id, autoclear):
        """
        :type user_id: int
        :type autoclear: bool
        """
        self.id = user_id
        self.data = {'self_msg_send': 0,
                     'chat_msg_send': 0}

        self.main_page = ''  # type: str
        self.sub_pages = []  # type: List[str]
        self.page_data = {}  # type: Dict[str]
        self.pages_url = ''  # type: str

        self.main_page = 'entry'
        self.autoclear = autoclear


    def change_page(self, page, *subpages):
        """
        :type page: str
        :type subpages: str
        """
        if self.autoclear:
            self.page_data.clear()

        self.main_page = page
        self.sub_pages = list(subpages)
        self.pages_url = f'{self.main_page}/{"/".join(self.sub_pages)}'


    def change_path(self, new_path):
        """
        :type new_path: str
        """
        if '/' in new_path:
            old_main_page = self.main_page
            self.main_page = new_path[:new_path.index('/')]

            if old_main_page != self.main_page and self.autoclear:
                self.page_data.clear()

            new_path = new_path[new_path.index('/') + 1:]

            self.sub_pages = []
            while '/' in new_path:
                new_sub = new_path[:new_path.index('/')]
                new_path = new_path[new_path.index('/') + 1:]
                self.sub_pages.append(new_sub)

            self.sub_pages.append(new_path)

        else:
            old_main_page = self.main_page

            self.main_page = new_path

            if old_main_page != self.main_page and self.autoclear:
                self.page_data.clear()
        self.pages_url = f'{self.main_page}/{"/".join(self.sub_pages)}'


    def on_new_message(self, in_chat):
        """
        :type in_chat: bool
        """

        if in_chat:
            self.data['chat_msg_send'] += 1
        else:
            self.data['self_msg_send'] += 1


    def __str__(self):
        return f'User<{self.id} in {"/"+self.pages_url if self.pages_url == "" else "/start"} messages: ' \
               f'{self.data["self_msg_send"]}, {self.data["chat_msg_send"]}>'


    def __repr__(self):
        return self.__str__()
