from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from pathlib import Path
from pydantic import BaseModel
import os

load_dotenv(override=True)

# ========== Configuration ==========
name = "Nima Ghorbani"
openai_client = OpenAI()

gemini = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ========== Load Profile Data ==========

def load_profile_data():

    current_dir = Path(__file__).parent

    project_root = current_dir.parent

    pdf_path = project_root / "assets" / "linkedin.pdf"
    summary_path = project_root / "assets" / "summary.txt"


    reader = PdfReader(pdf_path)
    linkedin = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text

    with open(summary_path, "r", encoding="utf-8") as f:
        summary = f.read()
    
    return linkedin, summary

linkedin, summary = load_profile_data()

# ========== System Prompt ==========
system_prompt_template = """
You are acting as {name}. You are answering questions on {name}'s website, particularly those related to {name}'s career, background, skills, and experience.

You are provided with a summary of {name}'s background and LinkedIn profile, which you can use to inform your responses.

Be professional, succinct, engaging, and conversational — as if you're speaking with a potential client or future employer who discovered the website. Keep your responses short and to the point.

If a user asks a question you cannot confidently answer, use the `record_unknown_question` tool to log the question — even if it seems trivial or unrelated to {name}'s career.

If the user is engaging in discussion, try to steer them toward getting in touch via email. Ask for their email and a name and log it using the `record_user_details` tool along with a brief note about the conversation and why they might be interested in connecting.

## Summary:
{summary}

## LinkedIn Profile:
{linkedin}

Use this context to chat with the user, and always stay in character as {name}.
"""
                        
system_prompt = system_prompt_template.format(
    name=name,
    summary=summary,
    linkedin=linkedin
)

# ========== Evaluation Model ==========

class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str
    
evaluator_system_prompt_template = """You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
Strictly avoid any personal details about the User or Agent. \
The response should be concise and to the point, and should not include any unnecessary formulation. \
The Agent is playing the role of {name} and is representing {name} on their website. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
The Agent has been provided with context on {name} in the form of their summary and LinkedIn details. Here's the information:
## Summary:
{summary}

## LinkedIn Profile:
{linkedin}

With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback.
"""

evaluator_system_prompt = evaluator_system_prompt_template.format(
    name=name,
    summary=summary,
    linkedin=linkedin
)