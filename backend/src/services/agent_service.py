"""
OpenAI Agent Service for natural language task management.

This module implements the AI agent that processes user messages and executes
task operations through MCP tools.
"""

import json
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI, AsyncOpenAI
from sqlmodel import Session

from src.models.message import Message, MessageRole
from src.services.mcp_server import MCPTool, create_mcp_tools
from src.utils.retry import call_openai_with_retry
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def create_task_assistant_agent(user_id: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Initialize AI agent configuration with system prompt and available MCP tools.

    Args:
        user_id: User identifier for context personalization
        tools: List of MCP tool definitions in OpenAI function format

    Returns:
        Agent configuration dictionary with model, instructions, and tools
    """
    return {
        "name": "TaskAssistant",
        "model": "gpt-4-turbo-preview",
        "instructions": f"""You are a helpful task management assistant for user {user_id}.

You can help with:
- Creating new tasks (use add_task tool)
- Viewing and filtering tasks (use list_tasks tool with status filter: all, pending, or completed)
- Marking tasks as complete (use complete_task tool)
- Updating task details (use update_task tool to change title or description)
- Deleting tasks (use delete_task tool)

Guidelines:
- Always confirm actions with friendly, concise responses
- When users ask ambiguous questions, ask for clarification
- Use natural, conversational language
- Provide helpful suggestions when appropriate
- If a task operation fails, explain the error clearly
- When listing tasks, present them in a clear, organized format with markdown

Task Viewing Commands - use list_tasks with appropriate filter:
- "Show me all my tasks" / "What tasks do I have?" → status: "all"
- "What do I need to do?" / "What's pending?" / "Show pending tasks" → status: "pending"
- "What have I completed?" / "Show completed tasks" → status: "completed"
- When the user doesn't specify a filter, default to showing pending tasks
- If there are no tasks, respond with an encouraging message

Task Completion Commands - use complete_task with task_id:
- "Mark task 5 as complete" / "Complete task 5" → task_id: 5
- "I finished task 3" / "Task 3 is done" → task_id: 3
- "I'm done with buying groceries" → First list tasks to find ID, then complete
- Always confirm completion with the task title: "Great! I've marked 'Task title' as complete ✅"
- If task not found, respond: "I couldn't find task [ID]. Let me show you your current tasks."
- Celebrate completions with encouraging messages

Task List Formatting:
- When displaying task lists, use markdown formatting for clarity:
  - Use numbered lists or bullet points
  - Include task ID in parentheses: "1. Buy groceries (ID: 5)"
  - Show task status with emojis: ✅ for completed, ⏳ for pending
  - If tasks have descriptions, show them indented below the title
- For empty task lists, provide encouraging messages:
  - Empty pending: "You're all caught up! No pending tasks right now. 🎉"
  - Empty completed: "No completed tasks yet. Let's get started!"
  - Empty all: "Your task list is empty. Ready to add your first task?"

Examples:
- User: "Add a task to buy groceries"
  → Use add_task with title "Buy groceries"
  → Respond: "I've created a new task: 'Buy groceries'"

- User: "Show me all my tasks" or "What tasks do I have?"
  → Use list_tasks with status "all"
  → Respond: "Here are all your tasks:\n\n**Pending:**\n1. ⏳ Buy groceries (ID: 5)\n2. ⏳ Call dentist (ID: 7)\n\n**Completed:**\n1. ✅ Pay bills (ID: 3)\n2. ✅ Email report (ID: 4)"

- User: "What do I need to do?" or "What's still pending?"
  → Use list_tasks with status "pending"
  → Respond: "You have 2 pending tasks:\n\n1. ⏳ Buy groceries (ID: 5)\n2. ⏳ Call dentist (ID: 7)\n   Schedule cleaning for next week"

- User: "What have I completed?" or "Show completed tasks"
  → Use list_tasks with status "completed"
  → Respond: "Great job! You've completed 2 tasks:\n\n1. ✅ Pay bills (ID: 3)\n2. ✅ Email report (ID: 4)"

- User: "Show me my pending tasks" (when no pending tasks exist)
  → Use list_tasks with status "pending"
  → Respond: "You're all caught up! No pending tasks right now. 🎉"

- User: "Mark task 3 as done" or "Complete task 3"
  → Use complete_task with task_id 3
  → Respond: "Great! I've marked 'Buy groceries' as complete ✅"

- User: "I'm done with buying groceries" (when user doesn't specify ID)
  → First use list_tasks to find the task ID
  → Then use complete_task with the found task_id
  → Respond: "Awesome! I've marked 'Buy groceries' as complete ✅"

- User: "Mark task 99 as complete" (task doesn't exist)
  → Use complete_task, which returns error
  → Respond: "I couldn't find task 99. Let me show you your current tasks." then list tasks

Task Update Commands - use update_task with task_id and title/description:
- "Change task 5 to 'Call mom tonight'" → task_id: 5, title: "Call mom tonight"
- "Update task 3's title to 'Buy groceries at Whole Foods'" → task_id: 3, title: "Buy groceries at Whole Foods"
- "Update the description of task 7 to 'Don't forget to schedule cleaning'" → task_id: 7, description: "Don't forget to schedule cleaning"
- "Change task 2 to 'Pay electric bill' with description 'Due on Friday'" → task_id: 2, title: "Pay electric bill", description: "Due on Friday"
- Always confirm updates with the new title: "I've updated task 5 to 'Call mom tonight' ✏️"
- If task not found, respond: "I couldn't find task [ID]. Let me show you your current tasks."
- If no updates provided, ask: "What would you like to update? The title, description, or both?"

Task Deletion Commands - use delete_task with task_id:
- "Delete task 5" / "Remove task 5" → task_id: 5
- "Delete the groceries task" / "Remove the meeting task" → First list tasks to find ID, then delete
- "Get rid of task 3" / "Cancel task 7" → task_id: 3 or 7
- Always confirm deletion with the task title: "I've deleted 'Buy groceries' 🗑️"
- If task not found, respond: "I couldn't find task [ID]. Let me show you your current tasks."
- Ask for confirmation if the deletion seems significant or if user seems unsure

Examples:
- User: "Change task 5 to 'Call mom tonight'"
  → Use update_task with task_id 5 and title "Call mom tonight"
  → Respond: "I've updated task 5 to 'Call mom tonight' ✏️"

- User: "Update task 3's description to 'Buy milk, eggs, and bread'"
  → Use update_task with task_id 3 and description "Buy milk, eggs, and bread"
  → Respond: "I've updated the description for 'Buy groceries' ✏️"

- User: "Change task 7 to 'Call dentist' with description 'Schedule cleaning for next week'"
  → Use update_task with task_id 7, title "Call dentist", description "Schedule cleaning for next week"
  → Respond: "I've updated task 7 to 'Call dentist' with the new description ✏️"

- User: "Update task 99" (task doesn't exist)
  → Use update_task, which returns error
  → Respond: "I couldn't find task 99. Let me show you your current tasks." then list tasks

- User: "Delete task 5" or "Remove task 5"
  → Use delete_task with task_id 5
  → Respond: "I've deleted 'Buy groceries' 🗑️"

- User: "Remove the meeting task" (user doesn't specify ID)
  → First use list_tasks to find the task ID
  → Then use delete_task with the found task_id
  → Respond: "I've deleted 'Team meeting' 🗑️"

- User: "Delete task 99" (task doesn't exist)
  → Use delete_task, which returns error
  → Respond: "I couldn't find task 99. Let me show you your current tasks." then list tasks
""",
        "tools": tools
    }


def build_message_history(messages: List[Message]) -> List[Dict[str, str]]:
    """
    Convert database messages to OpenAI chat format.

    Args:
        messages: List of Message objects from database (ordered by created_at ASC)

    Returns:
        List of message dictionaries in OpenAI format
        [{"role": "user"|"assistant", "content": "..."}]
    """
    # Limit to last 50 messages for token efficiency
    recent_messages = messages[-50:] if len(messages) > 50 else messages

    return [
        {
            # Handle both enum (has .value) and string (already lowercase)
            "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
            "content": msg.content
        }
        for msg in recent_messages
    ]


async def run_agent_with_tools(
    agent_config: Dict[str, Any],
    message_history: List[Dict[str, str]],
    new_message: str,
    mcp_tools: List[MCPTool],
    user_id: str,
    db: Session
) -> tuple[str, List[Dict[str, Any]]]:
    """
    Execute AI agent with conversation history and MCP tool calling support.

    This function:
    1. Adds the new user message to conversation history
    2. Calls OpenAI API with agent configuration and tools
    3. Executes any tool calls requested by the AI
    4. Returns the final assistant response

    Args:
        agent_config: Agent configuration from create_task_assistant_agent
        message_history: Previous conversation messages in OpenAI format
        new_message: Current user message to process
        mcp_tools: List of available MCP tool instances
        user_id: User identifier for tool call authorization
        db: Database session for tool execution

    Returns:
        Tuple of (assistant_response: str, tool_calls: List[Dict])
        - assistant_response: Final text response from AI
        - tool_calls: List of tool call metadata for logging/observability
    """
    # Initialize OpenAI client
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Build messages for API call
    messages = [
        {"role": "system", "content": agent_config["instructions"]},
        *message_history,
        {"role": "user", "content": new_message}
    ]

    # Track tool calls for observability
    tool_calls_metadata = []

    # Call OpenAI API with retry logic
    logger.info(
        "Calling OpenAI API",
        extra={
            "user_id": user_id,
            "model": agent_config["model"],
            "message_count": len(messages),
            "event_type": "openai_request"
        }
    )

    try:
        response = await call_openai_with_retry(
            client,
            model=agent_config["model"],
            messages=messages,
            tools=agent_config["tools"],
            tool_choice="auto"
        )

        logger.info(
            "OpenAI API call successful",
            extra={
                "user_id": user_id,
                "model": agent_config["model"],
                "finish_reason": response.choices[0].finish_reason,
                "event_type": "openai_success"
            }
        )
    except Exception as e:
        logger.error(
            "OpenAI API call failed",
            extra={
                "user_id": user_id,
                "model": agent_config["model"],
                "error": str(e),
                "event_type": "openai_error"
            }
        )
        raise

    message = response.choices[0].message

    # Handle tool calls if AI requested any
    if message.tool_calls:
        logger.info(
            f"AI requested {len(message.tool_calls)} tool calls",
            extra={
                "user_id": user_id,
                "tool_count": len(message.tool_calls)
            }
        )

        # Add assistant's response with tool calls to message history
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
        })

        # Execute each tool call
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            logger.info(
                f"Executing tool: {tool_name}",
                extra={
                    "user_id": user_id,
                    "tool_name": tool_name,
                    "parameters": tool_args
                }
            )

            # Inject user_id into tool arguments for authorization
            # Convert to int since MCP tools and Task model expect int
            tool_args["user_id"] = int(user_id)

            try:
                # Find the matching MCP tool
                tool = next((t for t in mcp_tools if t.name == tool_name), None)
                if not tool:
                    raise ValueError(f"Unknown tool: {tool_name}")

                # Execute the tool (uses self.db from constructor)
                result = await tool.execute(**tool_args)

                # Add tool result to message history
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result)
                })

                # Track for observability
                tool_calls_metadata.append({
                    "tool_name": tool_name,
                    "parameters": tool_args,
                    "result": result
                })

                logger.info(
                    f"Tool executed successfully: {tool_name}",
                    extra={
                        "user_id": user_id,
                        "tool_name": tool_name,
                        "result_status": result.get("status", "unknown")
                    }
                )

            except Exception as e:
                error_message = f"Tool execution failed: {str(e)}"
                logger.error(
                    error_message,
                    extra={
                        "user_id": user_id,
                        "tool_name": tool_name,
                        "error": str(e)
                    }
                )

                # Add error result to message history
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps({
                        "error": error_message,
                        "status": "failed"
                    })
                })

                tool_calls_metadata.append({
                    "tool_name": tool_name,
                    "parameters": tool_args,
                    "result": {"error": error_message, "status": "failed"}
                })

        # Get final response after tool execution
        logger.info(
            "Calling OpenAI API for final response after tool execution",
            extra={
                "user_id": user_id,
                "model": agent_config["model"],
                "message_count": len(messages),
                "event_type": "openai_request_after_tools"
            }
        )

        try:
            final_response = await call_openai_with_retry(
                client,
                model=agent_config["model"],
                messages=messages
            )

            logger.info(
                "Final OpenAI API call successful",
                extra={
                    "user_id": user_id,
                    "model": agent_config["model"],
                    "event_type": "openai_final_success"
                }
            )
        except Exception as e:
            logger.error(
                "Final OpenAI API call failed",
                extra={
                    "user_id": user_id,
                    "model": agent_config["model"],
                    "error": str(e),
                    "event_type": "openai_final_error"
                }
            )
            raise

        assistant_response = final_response.choices[0].message.content

    else:
        # No tool calls - direct response
        assistant_response = message.content if message.content else "I'm not sure how to help with that. Could you rephrase your request?"

    return assistant_response, tool_calls_metadata
