from typing import Optional

class Message:
    def __init__(
        self,
        id: str,
        name: str,
        message: str,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        self.name: str = name
        self.message: str = message
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Message):
            return self.id == o.id
        
        return False
