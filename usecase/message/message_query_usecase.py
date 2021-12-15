from abc import ABC, abstractclassmethod
from typing import List, Optional

from domain.message import MessageNotFoundError, MessagesNotFoundError

from .message_query_model import MessageReadModel
from .message_query_service import MessageQueryService


class MessageQueryUseCase(ABC):
    @abstractclassmethod
    def fetch_message_by_id(self, id: str) -> Optional[MessageReadModel]:
        raise NotImplementedError

    @abstractclassmethod
    def fetch_messages(self) -> List[MessageReadModel]:
        raise NotImplementedError
    
class MessageQueryUseCaseImpl(MessageQueryUseCase):
    def __init__(self, message_query_service: MessageQueryService):
        self.message_query_service: MessageQueryService = message_query_service

    def fetch_message_by_id(self, id: str) -> Optional[MessageReadModel]:
        try:
            message = self.message_query_service.find_by_id(id)
            if message is None:
                raise MessageNotFoundError
        except:
            raise
        
        return message
    
    def fetch_messages(self) -> List[MessageReadModel]:
        try:
            messages = self.message_query_service.find_all()
            if messages is None:
                raise MessagesNotFoundError
        except:
            raise
        
        return messages
    


