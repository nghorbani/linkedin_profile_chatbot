from linkedin_profile_chatbot.core import openai_client, system_prompt, evaluator_system_prompt, gemini, Evaluation
from linkedin_profile_chatbot.agent_tools import tools, handle_tool_calls
from loguru import logger

def evaluator_user_prompt(reply, message, history):
    user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
    user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
    user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
    user_prompt += "Please evaluate the response, replying with whether it is acceptable and your feedback."
    return user_prompt

def evaluate(reply, message, history) -> Evaluation:

    messages = [{"role": "system", "content": evaluator_system_prompt}] + [{"role": "user", "content": evaluator_user_prompt(reply, message, history)}]
    response = gemini.beta.chat.completions.parse(model="gemini-2.0-flash", messages=messages, response_format=Evaluation)
    return response.choices[0].message.parsed

def chat(message, history):
    messages = [{"role":"system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    evaluation_passed = False
    
    while not evaluation_passed:
        # First, handle the conversation and tool calls until we get a final response
        conversation_done = False
        current_messages = messages.copy()
        
        while not conversation_done:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=current_messages, 
                tools=[{"type": "function", "function": v} for v in tools.values()]
            )
            
            finish_reason = response.choices[0].finish_reason
            
            if finish_reason == "tool_calls":
                message_with_tools = response.choices[0].message
                tool_calls = message_with_tools.tool_calls
                results = handle_tool_calls(tool_calls)
                current_messages.append(message_with_tools)
                current_messages.extend(results)
            else:
                conversation_done = True
        
        # Now we have the final response, evaluate it
        final_reply = response.choices[0].message.content
        evaluation = evaluate(final_reply, message, history)
        
        if evaluation.is_acceptable:
            logger.info("Passed evaluation - returning reply")
            evaluation_passed = True
        else:
            logger.warning(f"Failed evaluation - retrying: {evaluation.feedback}")
            # Reset messages and try again with feedback
            updated_system_prompt = system_prompt + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
            updated_system_prompt += f"## Your attempted answer:\n{final_reply}\n\n"
            updated_system_prompt += f"## Reason for rejection:\n{evaluation.feedback}\n\n"
            messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
    
    return final_reply
