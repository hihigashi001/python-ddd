class MessageNotFoundError(Exception):
    message = "メッセージが見つかりません。"

    def __str__(self):
        return MessageNotFoundError.message


class MessagesNotFoundError(Exception):
    message = "メッセージ一覧が見つかりません。"

    def __str__(self):
        return MessagesNotFoundError.message
