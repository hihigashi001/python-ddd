from abc import ABC, abstractclassmethod
from typing import Optional, cast
import shortuuid
from domain.message import (
    Message,
    MessageNotFoundError,
    MessageRepository,
)

from .message_command_model import MessageCreateModel, MessageUpdateModel
from .message_query_model import MessageReadModel

class MessageCommandUseCaseUnitOfWork(ABC):
    message_repository: MessageRepository
    
    @abstractclassmethod
    def begin(self):
        raise NotImplementedError
    
    @abstractclassmethod
    def commit(self):
        raise NotImplementedError
    
    @abstractclassmethod
    def rollback(self):
        raise NotImplementedError
    
class MessageCommandUseCase(ABC):
    @abstractclassmethod
    def create_message(self, data: MessageCreateModel) -> Optional[MessageReadModel]:
        raise NotImplementedError
    
    @abstractclassmethod
    def update_message(self, id: str, data: MessageCreateModel) -> Optional[MessageReadModel]:
        raise NotImplementedError
    
    @abstractclassmethod
    def delete_message_by_id(self, id: str):
        raise NotImplementedError

class MessageCommandUseCaseImpl(MessageCommandUseCase):
    def __init__(
        self,
        uow: MessageCommandUseCaseUnitOfWork,
    ):
        self.uow: MessageCommandUseCaseUnitOfWork = uow
        
    def create_message(self, data: MessageCreateModel) -> Optional[MessageReadModel]:
        try:
            uuid = shortuuid.uuid()
            message = Message(id=uuid, name=data.name, message=data.message)
            
            self.uow.message_repository.create(message)
            self.uow.commit()
            
            created_message = self.uow.message_repository.find_by_id(uuid)
        except:
            self.uow.rollback()
            raise
        
        return MessageReadModel.from_entity(Message, created_message)
    
    def update_message(self, id: str, data: MessageUpdateModel) -> Optional[MessageReadModel]:
        try:
            existing_message = self.uow.message_repository.find_by_id(id)
            if existing_message is None:
                raise MessageNotFoundError
            
            message = Message(
                id=id, 
                name=data.name, 
                message=data.message,
            )
            
            self.uow.message_repository.update(message)

            update_message = self.uow.message_repository.find_by_id(message.id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise
        
        return MessageReadModel.from_entity(cast(Message, update_message))

    def delete_message_by_id(self, id: str):
        try:
            existing_book = self.uow.message_repository.find_by_id(id)
            if existing_book is None:
                raise MessageNotFoundError
            
            self.uow.message_repository.delete_by_id(id)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise