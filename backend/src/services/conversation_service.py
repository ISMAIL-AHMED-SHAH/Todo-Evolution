"""Conversation service for AI chatbot feature."""
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from src.models.conversation import Conversation
from src.models.message import Message, MessageRole
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_conversation_title(first_message: str, max_length: int = 50) -> str:
    """
    Generate conversation title from first user message.

    Args:
        first_message: First message content
        max_length: Maximum title length (default: 50)

    Returns:
        Title string (truncated with ellipsis if needed)

    Example:
        >>> generate_conversation_title("Add a task to buy groceries")
        "Add a task to buy groceries"
        >>> generate_conversation_title("I need to remember to pay bills on Friday and also call mom")
        "I need to remember to pay bills on Friday and..."
    """
    # Remove extra whitespace
    cleaned = " ".join(first_message.split())

    # Truncate with ellipsis
    if len(cleaned) <= max_length:
        return cleaned

    return cleaned[:max_length - 3] + "..."


def create_conversation(
    db: Session,
    user_id: str,
    title: str
) -> Conversation:
    """
    Create a new conversation.

    Args:
        db: Database session
        user_id: User identifier
        title: Conversation title

    Returns:
        Created conversation

    Example:
        ```python
        conversation = create_conversation(
            db=db,
            user_id="user123",
            title="Shopping list discussion"
        )
        ```
    """
    conversation = Conversation(
        user_id=user_id,
        title=title
    )
    db.add(conversation)
    db.flush()  # Get ID without committing - allows caller to commit atomically

    logger.info(
        "Conversation created (pending commit)",
        extra={
            "user_id": user_id,
            "conversation_id": str(conversation.id),
            "event_type": "conversation_created"
        }
    )

    return conversation


def create_conversation_with_message(
    db: Session,
    user_id: str,
    first_message: str
) -> Conversation:
    """
    Create a new conversation with the first user message.

    This function:
    1. Generates a title from the first message
    2. Creates the conversation
    3. Creates the first user message

    Args:
        db: Database session
        user_id: User identifier
        first_message: First user message content

    Returns:
        Created conversation with first message

    Example:
        ```python
        conversation = await create_conversation_with_message(
            db=db,
            user_id="user123",
            first_message="Add a task to buy groceries"
        )
        ```
    """
    # Generate title from first message
    title = generate_conversation_title(first_message)

    # Create conversation (flush only, no commit yet)
    conversation = create_conversation(db, user_id, title)

    # Create first user message
    # Use .value to get lowercase string ('user') for database check constraint
    message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role=MessageRole.USER.value,
        content=first_message
    )
    db.add(message)

    # Single atomic commit for both conversation + message
    db.commit()
    db.refresh(conversation)

    logger.info(
        "Conversation created with first message",
        extra={
            "user_id": user_id,
            "conversation_id": str(conversation.id),
            "event_type": "conversation_created_with_message"
        }
    )

    return conversation


def get_conversation(
    db: Session,
    conversation_id: UUID,
    user_id: str
) -> Optional[Conversation]:
    """
    Get a conversation by ID with ownership verification.

    Args:
        db: Database session
        conversation_id: Conversation UUID
        user_id: User identifier (for ownership check)

    Returns:
        Conversation if found and owned by user, None otherwise

    Example:
        ```python
        conversation = await get_conversation(
            db=db,
            conversation_id=UUID("..."),
            user_id="user123"
        )
        ```
    """
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = db.exec(statement)
    return result.first()


def get_user_conversations(
    db: Session,
    user_id: str,
    limit: int = 50
) -> List[Conversation]:
    """
    Get all conversations for a user (chronological order, newest first).

    Query optimization:
    - Uses ix_conversations_user_id index for WHERE clause
    - Uses ix_conversations_created_at index (DESC) for ORDER BY clause
    - Combined with LIMIT, this provides fast retrieval

    Args:
        db: Database session
        user_id: User identifier
        limit: Maximum number of conversations to return (default: 50)

    Returns:
        List of conversations

    Example:
        ```python
        conversations = await get_user_conversations(
            db=db,
            user_id="user123",
            limit=10
        )
        ```
    """
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .limit(limit)
    )
    result = db.exec(statement)
    conversations = list(result.all())

    logger.info(
        "User conversations loaded",
        extra={
            "user_id": user_id,
            "conversation_count": len(conversations),
            "event_type": "user_conversations_loaded"
        }
    )

    return conversations


def get_conversation_messages(
    db: Session,
    conversation_id: UUID,
    limit: int = 50
) -> List[Message]:
    """
    Get messages for a conversation (chronological order, oldest first).

    This fetches the last N messages for building AI context.

    Query optimization:
    - Uses ix_messages_conversation_id index for WHERE clause
    - Uses ix_messages_created_at index for ORDER BY clause
    - Combined with LIMIT, this provides fast retrieval even with many messages

    Args:
        db: Database session
        conversation_id: Conversation UUID
        limit: Maximum number of messages to return (default: 50)

    Returns:
        List of messages ordered by created_at ASC

    Example:
        ```python
        messages = await get_conversation_messages(
            db=db,
            conversation_id=UUID("..."),
            limit=50
        )
        ```
    """
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .limit(limit)
    )
    result = db.exec(statement)
    messages = list(result.all())

    logger.info(
        "Conversation history loaded",
        extra={
            "conversation_id": str(conversation_id),
            "message_count": len(messages),
            "event_type": "conversation_history_loaded"
        }
    )

    return messages


def add_message(
    db: Session,
    conversation_id: UUID,
    user_id: str,
    role: MessageRole,
    content: str
) -> Message:
    """
    Add a message to a conversation.

    Args:
        db: Database session
        conversation_id: Conversation UUID
        user_id: User identifier
        role: Message role (USER or ASSISTANT)
        content: Message content

    Returns:
        Created message

    Example:
        ```python
        message = await add_message(
            db=db,
            conversation_id=UUID("..."),
            user_id="user123",
            role=MessageRole.USER,
            content="Add a task to buy groceries"
        )
        ```
    """
    # Use .value to get lowercase string ('user'/'assistant') for database check constraint
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role.value if hasattr(role, 'value') else role,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    # Update conversation updated_at timestamp
    statement = select(Conversation).where(Conversation.id == conversation_id)
    conversation = db.exec(statement).first()
    if conversation:
        conversation.updated_at = datetime.utcnow()
        db.add(conversation)
        db.commit()

    logger.info(
        "Message added to conversation",
        extra={
            "conversation_id": str(conversation_id),
            "user_id": user_id,
            "role": role.value,
            "message_length": len(content),
            "event_type": "message_added"
        }
    )

    return message


def verify_conversation_ownership(
    db: Session,
    conversation_id: UUID,
    user_id: str
) -> bool:
    """
    Verify that a user owns a conversation (security check).

    Args:
        db: Database session
        conversation_id: Conversation UUID
        user_id: User identifier

    Returns:
        True if user owns conversation, False otherwise

    Example:
        ```python
        if not await verify_conversation_ownership(db, conversation_id, user_id):
            raise HTTPException(status_code=403, detail="Forbidden")
        ```
    """
    statement = select(Conversation.id).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = db.exec(statement)
    return result.first() is not None
