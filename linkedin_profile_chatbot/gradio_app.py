import gradio as gr
from .chat import chat

# ========== Gradio Interface ==========
if __name__ == "__main__":
    gr.ChatInterface(chat, type="messages").launch()
