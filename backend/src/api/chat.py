"""
Chat API endpoint for AI-powered task management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlmodel import Session
from asyncio import TimeoutError
from sqlalchemy.exc import OperationalError, SQLAlchemyError, IntegrityError
from openai import APIError, AuthenticationError, RateLimitError

from ..database import get_session
from ..auth.jwt_handler import jwt_bearer
from ..services.queue_service import get_queue_service, UserRequestQueue
from ..services.conversation_service import (
    create_conversation_with_message,
    get_conversation_messages,
    verify_conversation_ownership,
    get_user_conversations,
)
from ..services.agent_service import run_agent_with_tools
from ..models.message import Message, MessageRole
from ..models.conversation import Conversation
from ..utils.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()


# Pydantic Models
class ChatRequest(BaseModel):
    """Chat request payload"""
    message: str = Field(..., min_length=1, max_length=5000, description="User's message")
    conversation_id: Optional[UUID] = Field(None, description="Optional conversation ID. Creates new if not provided")

    @field_validator('message')
    @classmethod
    def validate_message_not_whitespace(cls, v: str) -> str:
        """Validate message is not empty or whitespace only"""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()


class ToolCallMetadata(BaseModel):
    """Metadata about a tool call made by the AI"""
    tool_name: str = Field(..., description="Name of the tool that was called")
    parameters: Dict[str, Any] = Field(..., description="Parameters passed to the tool")
    result: Optional[Dict[str, Any]] = Field(None, description="Result returned by the tool")


class ChatResponse(BaseModel):
    """Chat response payload"""
    conversation_id: UUID = Field(..., description="ID of the conversation")
    response: str = Field(..., description="AI assistant's response")
    tool_calls: List[ToolCallMetadata] = Field(default_factory=list, description="List of tool calls made during processing")


class ConversationSummary(BaseModel):
    """Summary of a conversation for list display"""
    id: UUID = Field(..., description="Conversation ID")
    title: str = Field(..., description="Conversation title")
    created_at: str = Field(..., description="Creation timestamp (ISO format)")
    updated_at: str = Field(..., description="Last update timestamp (ISO format)")


class ConversationsListResponse(BaseModel):
    """Response containing list of user's conversations"""
    conversations: List[ConversationSummary] = Field(..., description="List of user conversations")


# Endpoint handlers
async def process_chat_message(
    user_id: str,
    request: ChatRequest
) -> ChatResponse:
    """
    Process a chat message through the AI agent pipeline.

    Steps:
    1. Create or verify conversation
    2. Fetch conversation history (last 50 messages)
    3. Store user message
    4. Invoke AI agent with tools
    5. Store assistant response
    6. Return response with metadata
    """
    # Import here to avoid circular imports
    from ..database import get_db_session

    # Create fresh database session for this queued request
    # This ensures the session is not stale from async queue delays
    with get_db_session() as db:
        try:
            logger.info("Processing chat message", extra={
                "user_id": user_id,
                "conversation_id": str(request.conversation_id) if request.conversation_id else None,
                "message_length": len(request.message)
            })

            # Step 1: Handle conversation_id (create new or verify ownership)
            conversation_id = request.conversation_id

            if conversation_id is None:
                # Create new conversation with first message
                logger.info("Creating new conversation", extra={"user_id": user_id})
                conversation = create_conversation_with_message(
                    db=db,
                    user_id=user_id,
                    first_message=request.message
                )
                conversation_id = conversation.id

                # The first message was already stored by create_conversation_with_message
                # Now we need to invoke the AI agent
                # Use .value for database check constraint compatibility
                conversation_history = [
                    Message(
                        conversation_id=conversation_id,
                        user_id=user_id,
                        role=MessageRole.USER.value,
                        content=request.message
                    )
                ]
            else:
                # Verify user owns the conversation
                logger.info("Verifying conversation ownership", extra={
                    "user_id": user_id,
                    "conversation_id": str(conversation_id)
                })

                is_owner = verify_conversation_ownership(
                    db=db,
                    conversation_id=conversation_id,
                    user_id=user_id
                )

                if not is_owner:
                    logger.warning("Conversation ownership verification failed", extra={
                        "user_id": user_id,
                        "conversation_id": str(conversation_id)
                    })
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You do not have access to this conversation"
                    )

                # Fetch conversation history (last 50 messages)
                logger.info("Fetching conversation history", extra={
                    "conversation_id": str(conversation_id)
                })
                conversation_history = get_conversation_messages(
                    db=db,
                    conversation_id=conversation_id,
                    limit=50
                )

                # Store user message
                logger.info("Storing user message", extra={
                    "conversation_id": str(conversation_id)
                })
                # Use .value for database check constraint compatibility
                user_message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role=MessageRole.USER.value,
                    content=request.message
                )
                db.add(user_message)
                db.commit()
                db.refresh(user_message)

                # Add to conversation history for AI context
                conversation_history.append(user_message)

            # Step 2: Invoke AI agent with conversation context
            logger.info("Invoking AI agent", extra={
                "conversation_id": str(conversation_id),
                "history_length": len(conversation_history)
            })

            # Import needed functions from agent service
            from ..services.agent_service import create_task_assistant_agent, build_message_history, run_agent_with_tools
            from ..services.mcp_server import create_mcp_tools

            # Create MCP tools with database session
            mcp_tools = create_mcp_tools(db)

            # Create agent configuration
            agent_config = create_task_assistant_agent(
                user_id=user_id,
                tools=[tool.to_openai_format() for tool in mcp_tools]
            )

            # Build message history in OpenAI format
            message_history_openai = build_message_history(conversation_history)

            # Run agent with tools
            agent_response, tool_calls = await run_agent_with_tools(
                agent_config=agent_config,
                message_history=message_history_openai,
                new_message=request.message,
                mcp_tools=mcp_tools,
                user_id=user_id,
                db=db
            )

            # Step 3: Store assistant response
            logger.info("Storing assistant response", extra={
                "conversation_id": str(conversation_id),
                "tool_calls_count": len(tool_calls)
            })

            # Use .value for database check constraint compatibility
            assistant_message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=MessageRole.ASSISTANT.value,
                content=agent_response
            )
            db.add(assistant_message)
            db.commit()

            # Step 4: Log tool calls
            for tool_call in tool_calls:
                logger.info("MCP tool called", extra={
                    "tool_name": tool_call.get("tool_name"),
                    "parameters": tool_call.get("parameters"),
                    "result": tool_call.get("result")
                })

            # Step 5: Return response
            logger.info("Chat message processed successfully", extra={
                "conversation_id": str(conversation_id)
            })

            return ChatResponse(
                conversation_id=conversation_id,
                response=agent_response,
                tool_calls=[
                    ToolCallMetadata(
                        tool_name=tc.get("tool_name", "unknown"),
                        parameters=tc.get("parameters", {}),
                        result=tc.get("result")
                    )
                    for tc in tool_calls
                ]
            )

        except HTTPException:
            # Re-raise HTTP exceptions (e.g., 403 Forbidden)
            raise

        except TimeoutError as e:
            logger.error("Request timeout", extra={
                "user_id": user_id,
                "error": str(e)
            }, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Request timed out. Please try again."
            )

        except RuntimeError as e:
            # Queue full error
            if "Too many pending requests" in str(e):
                logger.warning("Queue full", extra={
                    "user_id": user_id,
                    "error": str(e)
                })
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=str(e)
                )
            # Other runtime errors - log and return 500
            logger.error("Runtime error in chat", extra={
                "user_id": user_id,
                "error": str(e),
                "error_type": type(e).__name__
            }, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Runtime error: {str(e)}"
            )

        except OperationalError as e:
            # TRUE database connection failure - 503
            logger.error("Database connection error", extra={
                "user_id": user_id,
                "error": str(e),
                "error_type": "OperationalError"
            }, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection failed. Please try again in a moment."
            )

        except IntegrityError as e:
            # Database constraint violation - 400
            logger.error("Database integrity error", extra={
                "user_id": user_id,
                "error": str(e),
                "error_type": "IntegrityError"
            }, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity error. The operation could not be completed."
            )

        except SQLAlchemyError as e:
            # Other SQLAlchemy errors - 500 with real cause
            logger.error("Database error", extra={
                "user_id": user_id,
                "error": str(e),
                "error_type": type(e).__name__
            }, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {type(e).__name__}"
            )

        except AuthenticationError as e:
            # OpenAI authentication failure
            logger.error("OpenAI authentication error", extra={
                "user_id": user_id,
                "error": str(e)
            }, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service authentication failed. Please contact support."
            )

        except RateLimitError as e:
            # OpenAI rate limit
            logger.warning("OpenAI rate limit", extra={
                "user_id": user_id,
                "error": str(e)
            })
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="AI service is busy. Please try again in a moment."
            )

        except APIError as e:
            # Other OpenAI API errors
            logger.error("OpenAI API error", extra={
                "user_id": user_id,
                "error": str(e),
                "status_code": getattr(e, 'status_code', None)
            }, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI service error. Please try again."
            )

        except Exception as e:
            # Catch-all for unexpected errors - log full details, return 500
            logger.error("Unexpected error in chat", extra={
                "user_id": user_id,
                "error": str(e),
                "error_type": type(e).__name__
            }, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {type(e).__name__} - {str(e)}"
            )


def get_user_id_from_jwt(payload: dict = Depends(jwt_bearer)) -> str:
    """
    Extract user ID from JWT payload.

    Args:
        payload: Decoded JWT payload from jwt_bearer dependency

    Returns:
        User ID as string

    Raises:
        HTTPException: If user ID not found in payload
    """
    user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token"
        )
    return str(user_id)


@router.post("/api/{user_id}/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    token_user_id: str = Depends(get_user_id_from_jwt),
    queue_service: UserRequestQueue = Depends(get_queue_service)
):
    """
    Send a message to the AI chatbot and receive a response.

    - Creates a new conversation if conversation_id not provided
    - Verifies conversation ownership if conversation_id provided
    - Processes message through AI agent with MCP tools
    - Returns AI response with metadata about tool calls

    Args:
        user_id: User ID from path parameter
        request: Chat request with message and optional conversation_id
        token_user_id: User ID extracted from JWT token
        queue_service: Per-user request queue service

    Returns:
        ChatResponse with conversation_id, AI response, and tool call metadata

    Raises:
        400: Message too long or invalid format
        401: Invalid or missing JWT token
        403: User does not own the conversation
        429: Rate limit exceeded (after retries)
        500: Server error
    """
    # Validate user_id matches JWT token
    if user_id != token_user_id:
        logger.warning("User ID mismatch", extra={
            "path_user_id": user_id,
            "token_user_id": token_user_id
        })
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch. You can only send messages as yourself."
        )

    # Submit to per-user queue for sequential processing
    logger.info("Submitting chat request to queue", extra={"user_id": user_id})

    # enqueue signature: enqueue(user_id, handler, *args, **kwargs)
    # process_chat_message signature: process_chat_message(user_id, request)
    # Note: DB session is created fresh inside process_chat_message to avoid stale connections
    response = await queue_service.enqueue(
        user_id,               # Queue user_id (for queue isolation)
        process_chat_message,  # Handler function
        user_id,               # First arg for process_chat_message
        request                # Second arg for process_chat_message
    )

    return response


@router.get("/api/{user_id}/conversations", response_model=ConversationsListResponse, status_code=status.HTTP_200_OK)
async def list_conversations_endpoint(
    user_id: str,
    db: Session = Depends(get_session),
    token_user_id: str = Depends(get_user_id_from_jwt)
):
    """
    Get all conversations for a user.

    Returns a list of conversations ordered by created_at (newest first).

    Args:
        user_id: User ID from path parameter
        db: Database session
        token_user_id: User ID extracted from JWT token

    Returns:
        ConversationsListResponse with list of conversations

    Raises:
        401: Invalid or missing JWT token
        403: User ID mismatch
    """
    # Validate user_id matches JWT token
    if user_id != token_user_id:
        logger.warning("User ID mismatch in list conversations", extra={
            "path_user_id": user_id,
            "token_user_id": token_user_id
        })
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch. You can only view your own conversations."
        )

    logger.info("Fetching user conversations", extra={"user_id": user_id})

    conversations = get_user_conversations(db=db, user_id=user_id, limit=50)

    return ConversationsListResponse(
        conversations=[
            ConversationSummary(
                id=conv.id,
                title=conv.title,
                created_at=conv.created_at.isoformat(),
                updated_at=conv.updated_at.isoformat()
            )
            for conv in conversations
        ]
    )
