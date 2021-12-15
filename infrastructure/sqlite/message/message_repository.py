from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from domain.message import Message, MessageRepository
from usecase.message import MessageCommandUseCaseUnitOfWork

from .message_dto import MessageDTO

class MessageRepositoryImpl(MessageRepository):
    def __init__(self, session: Session):
        self.session: Session = session
        
    def find_by_id(self, id: str) -> Optional[Message]:
        try:
            message_dto = self.session.query(MessageDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise
        
        return message_dto.to_entity()
    
    
    def create(self, message: Message) -> Optional[Message]:
        message_dto = MessageDTO.from_entity(message)
        try:
            self.session.add(message_dto)
        except:
            raise
    
    
    def update(self, message: Message) -> Optional[Message]:
        message_dto = MessageDTO.from_entity(message)
        try:
            _message = self.session.query(MessageDTO).filter_by(id=message_dto.id).one()
            _message.name = message_dto.name
            _message.message = message_dto.message
            _message.updated_at = message_dto.updated_at
        except:
            raise
    
    
    def delete_by_id(self, id: str):
        try:
            self.session.query(MessageDTO).filter_by(id=id).delete()
        except:
            raise
        
        
class MessageCommandUseCaseUnitOfWorkImpl(MessageCommandUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        message_repository: MessageRepository,
    ):
        self.session: Session = session
        self.message_repository: MessageRepository = message_repository
        
        
    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()
        
    def rollback(self):
        self.session.rollback()


        