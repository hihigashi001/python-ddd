from pydantic import BaseModel, Field

class MessageCreateModel(BaseModel):
    name: str = Field(example="yamda jyuniti")
    message: str = Field(example="memo memo memo")


class MessageUpdateModel(BaseModel):
    name: str = Field(example="yamda jyuniti")
    message: str = Field(example="memo memo memo")

