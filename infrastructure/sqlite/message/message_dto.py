from datetime import datetime
from typing import Union

from sqlalchemy import Column, Integer, String

from domain.message import Message
from infrastructure.sqlite.database import Base
from usecase.message import MessageReadModel

def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class MessageDTO(Base):
    __tablename__ = "message"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    name: Union[str, Column] = Column(String, nullable=False)
    message: Union[str, Column] = Column(String, nullable=False)
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> Message:
        return Message(
            id=self.id,
            name=self.name,
            message=self.message,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        
    def to_read_model(self) -> MessageReadModel:
        return MessageReadModel(
            id=self.id,
            name=self.name,
            message=self.message,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        
    @staticmethod
    def from_entity(message: Message) -> "MessageDTO":
        now = unixtimestamp()
        return MessageDTO(
            id=message.id,
            name=message.name,
            message=message.message,
            created_at=now,
            updated_at=now,
        )
