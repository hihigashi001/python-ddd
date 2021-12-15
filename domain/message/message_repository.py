from abc import ABC, abstractmethod
from typing import List, Optional

from domain.message import Message


class MessageRepository(ABC):
    @abstractmethod
    def create(self, message: Message) -> Optional[Message]:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Message]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, message: Message) -> Optional[Message]:
        raise NotImplementedError
    
    @abstractmethod
    def delete_by_id(self, id: str):
        raise NotImplementedError