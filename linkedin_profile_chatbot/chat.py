from .core import openai_client, system_prompt
from .agent_tools import tools, handle_tool_calls

def chat(message, history):
    messages = [{"role":"system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    done = False
    
    while not done:
        response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=[{"type": "function", "function": v} for v in tools.values()])
        finish_reason = response.choices[0].finish_reason
        
        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    return response.choices[0].message.content
