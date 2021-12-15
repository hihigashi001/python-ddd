from typing import cast
from pydantic import BaseModel, Field
from domain.message import Message

class MessageReadModel(BaseModel):
    id: str = Field(example="1")
    name: str = Field(example="yamada jyuniti")
    message: str = Field(example="memo memo memo")
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    class Config:
        orm_mode = True
    
    @staticmethod
    def from_entity(message: Message) -> "MessageReadModel":
        return MessageReadModel(
            id=message.id,
            name=message.name,
            message=message.message,
            created_at=cast(int, message.created_at),
            updated_at=cast(int, message.updated_at),
        )