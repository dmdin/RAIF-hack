import vkchatbot
kek = vkchatbot.update.Update
# import vkchatbot vkchatbot.update.Update
from typing import Dict, Callable, Any
from vkchatbot.obj import User


class ConversationHandler:
    def __init__(self, entry_callback: Callable[[Any], Any],
                 pages: Dict[str, Callable[[Any], Any]]):

        self.pages = {'entry': entry_callback}
        self.pages.update(pages)


    def add_page(self, page_path, callback):
        """
        :type page_path: str
        :type callback: Callable[[Update], Any]]
        """
        if page_path not in self.pages.keys():
            self.pages[page_path] = callback
        else:
            raise ValueError(f'Page path {page_path} already exists')


    def get_callback(self, user) -> Callable[[Any], Any]:
        """
        :type user: User
        """

        if user.main_page == 'entry':
            return self.pages['entry']

        for page_path, callback in self.pages.items():
            slash_count = page_path.count('/')
            if len(user.sub_pages) >= slash_count:
                path = f'{user.main_page}/{"/".join(user.sub_pages)}'
                if path == page_path:
                    return callback

        if user.main_page in self.pages:
            return self.pages[user.main_page]

        raise ValueError(f'Page "{user.main_page}" not stated in self.pages')
