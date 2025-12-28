"""Message model for AI chatbot feature."""
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class MessageRole(str, Enum):
    """Message role enum: user or assistant."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """
    Individual message within a conversation (user or assistant).

    Validation Rules:
        - content length <= 5000 characters (enforced at model and database level)
        - role must be "user" or "assistant" (enum constraint)
        - conversation_id must reference existing conversation
        - user_id must match conversation owner (enforced at application level)
        - Messages are immutable (no updates or deletions, only creation)

    Relationships:
        - Many-to-one with Conversation (many messages belong to one conversation)
        - Many-to-one with User (many messages belong to one user)
    """
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True, nullable=False)
    user_id: str = Field(index=True, nullable=False)
    # Store as str to avoid SQLModel enum serialization issues (stores name instead of value)
    role: str = Field(nullable=False)
    content: str = Field(max_length=5000, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

    class Config:
        """Pydantic model configuration."""
        use_enum_values = True  # Store enum as string in database
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user123",
                "role": "user",
                "content": "Add a task to buy groceries",
                "created_at": "2025-12-22T10:00:00Z"
            }
        }
