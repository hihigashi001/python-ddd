from typing import Iterator, List

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm.session import Session

from domain.message import (
    MessageRepository,
    MessageNotFoundError,
    MessagesNotFoundError,
)
from infrastructure.sqlite.message import (
    MessageCommandUseCaseUnitOfWorkImpl,
    MessageQueryServiceImpl,
    MessageRepositoryImpl,
)
from infrastructure.sqlite.database import SessionLocal, create_tables
from usecase.message import (
    MessageCommandUseCase,
    MessageCommandUseCaseImpl,
    MessageCommandUseCaseUnitOfWork,
    MessageCreateModel,
    MessageQueryService,
    MessageQueryUseCase,
    MessageQueryUseCaseImpl,
    MessageReadModel,
    MessageUpdateModel,
    message_command_usecase,
)

create_tables()

router = APIRouter(prefix="/message")

def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        
def message_query_usecase(session: Session = Depends(get_session)) -> MessageQueryUseCase:
    message_query_service: MessageQueryService = MessageQueryServiceImpl(session)
    return MessageQueryUseCaseImpl(message_query_service)

def message_command_usecase(session: Session = Depends(get_session)) -> MessageCommandUseCase:
    message_repository: MessageRepository = MessageRepositoryImpl(session)
    uow: MessageCommandUseCaseUnitOfWork = MessageCommandUseCaseUnitOfWorkImpl(
        session, message_repository=message_repository
    )
    return MessageCommandUseCaseImpl(uow)


@router.post(
    "/",
    response_model=MessageReadModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_message(
    data: MessageCreateModel,
    message_command_usecase: MessageCommandUseCase = Depends(message_command_usecase),
):
    try:
        message = message_command_usecase.create_message(data)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
    return message


@router.get(
    "/",
    response_model=List[MessageReadModel],
    status_code=status.HTTP_200_OK,
)
async def get_messages(
    message_query_usecase: MessageQueryUseCase = Depends(message_query_usecase),
):
    try:
        messages = message_query_usecase.fetch_messages()
    
    except MessagesNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
        
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    
    return messages


@router.get(
    "/{message_id}",
    response_model=MessageReadModel,
    status_code=status.HTTP_200_OK,
)
async def get_message(
    message_id: str,
    message_query_usecase: MessageQueryUseCase = Depends(message_query_usecase),
):
    try:
        message = message_query_usecase.fetch_message_by_id(message_id)
    except MessageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
    return message


@router.put(
    "/{message_id}",
    response_model=MessageReadModel,
    status_code=status.HTTP_404_NOT_FOUND,
)
async def update_message(
    message_id: str,
    data: MessageUpdateModel,
    message_command_usecase: MessageCommandUseCase = Depends(message_command_usecase),
):
    try:
        update_message = message_command_usecase.update_message(message_id, data)
    except MessageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
    return update_message


@router.delete(
    "/{message_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_message(
    message_id: str,
    message_command_usecase: MessageCommandUseCase = Depends(message_command_usecase),
):
    try:
        message_command_usecase.delete_message_by_id(message_id)
    except MessageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )