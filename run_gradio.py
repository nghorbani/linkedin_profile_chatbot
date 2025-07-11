#!/usr/bin/env python3
"""
Simple script to run the Gradio interface for the LinkedIn Profile Chatbot
"""

if __name__ == "__main__":
    from linkedin_profile_chatbot.gradio_app import gr, chat
    gr.ChatInterface(chat, type="messages").launch()
