from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from usecase.message import MessageQueryService, MessageReadModel
from .message_dto import MessageDTO

class MessageQueryServiceImpl(MessageQueryService):
    def __init__(self, session: Session):
        self.session: Session = session
        
    def find_by_id(self, id: str) -> Optional[MessageReadModel]:
        try:
            message_dto = self.session.query(MessageDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise
        
        return message_dto.to_read_model()
    
    def find_all(self) -> List[MessageReadModel]:
        try:
            message_dtos = (
                self.session.query(MessageDTO)
                .order_by(MessageDTO.updated_at)
                .limit(100)
                .all()
            )
        except:
            raise
        
        if len(message_dtos) == 0:
            return []
        
        return list(map(lambda message_dto: message_dto.to_read_model(), message_dtos))