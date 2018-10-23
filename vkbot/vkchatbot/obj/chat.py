class Chat:
    def __init__(self, chat_id, invited_user, invited_date):
        """
        :type chat_id: int
        :type invited_user: int
        :type invited_date: int
        """
        self.id = chat_id
        self.invited_user = invited_user
        self.invited_date = invited_date
        self.data = {'messages_send': 0}


    def on_new_message(self):
        self.data['messages_send'] += 1


    def __str__(self):
        return f'Chat<{self.id} invited by {self.invited_user} messages: {self.data["messages_send"]}>'

    def __repr__(self):
        return self.__str__()
