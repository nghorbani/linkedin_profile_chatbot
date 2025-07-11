
import json
import os
from loguru import logger
from notifiers import get_notifier

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# ========== Push Notification Function ==========
def push_telegram():
    telegram = get_notifier('telegram')
    def push(message):
        logger.info(f"Pushing message: {message}")
        
        response = telegram.notify(
            token=telegram_token, 
            chat_id=telegram_chat_id, 
            message=message
        )
        json_response = {
            "status": 1 if response.status == 'Success' else 0,
        }
        
        return json_response
    return push

push = push_telegram()

def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "ok"}
    
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of the user"
            },
            "name": {
                "type": "string",
                "description": "The name of the user, if provided. try to get the user to provide a name if they haven't already"
            },
            "notes": {
                "type": "string",
                "description": "Any additional notes about the user and the conversation that is worth recording to give some context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered",
           },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = {"record_unknown_question_json": record_unknown_question_json,
         "record_user_details_json": record_user_details_json}

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    return results


