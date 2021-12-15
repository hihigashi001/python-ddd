from abc import ABC, abstractmethod
from typing import List, Optional

from .message_query_model import MessageReadModel

class MessageQueryService(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[MessageReadModel]:
        raise NotImplementedError
    
    @abstractmethod
    def find_all(self) -> List[MessageReadModel]:
        raise NotImplementedError
