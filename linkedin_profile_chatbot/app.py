import gradio as gr
from .chat import chat

# ========== Gradio Interface ==========
def create_gradio_interface():
    """Create and return the Gradio interface"""
    interface = gr.ChatInterface(
        chat, 
        type="messages",
        title="LinkedIn Profile Chatbot",
        description="Ask questions about the LinkedIn profile and get intelligent responses.",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 800px !important;
            margin: 0 auto !important;
        }
        """
    )
    return interface

if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch()
