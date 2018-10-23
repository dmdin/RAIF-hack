class MessageEvent:
    def __init__(self, params):
        """
        :type params: dict
        """

        self.date = params['date']                   # type: int
        self.from_id = params['from_id']             # type: int
        self.id = params['id']                       # type: int
        self.out = params['out']                     # type: int
        self.peer_id = params['peer_id']             # type: int
        self.text = params['text']                   # type: str
        self.fwd_messages = params['fwd_messages']   # type: list
        self.important = params['important']         # type: bool
        self.random_id = params['random_id']         # type: int
        self.is_hidden = params['is_hidden']         # type: bool
        self.attachments = params['attachments']     # type: list
        self.payload = params.get('payload')         # type: str
        self.conversation_message_id = params['conversation_message_id']  # type: int
