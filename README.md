# LinkedIn Profile Chatbot

A Gradio-based chatbot that can answer questions about your LinkedIn profile using AI. Upload your LinkedIn profile PDF and summary, then deploy to Hugging Face Spaces for easy sharing and embedding.

## Setup Instructions

### 1. Prepare Your Profile Data

#### Download Your LinkedIn Profile as PDF
1. Go to your LinkedIn profile page
2. Click the "More" button (three dots) in your profile section
3. Select "Save to PDF" from the dropdown menu
4. Save the PDF file as `linkedin.pdf`

#### Create a Profile Summary
1. Write a brief summary of your professional background, skills, and experience
2. Save this as a plain text file named `summary.txt`
3. Keep it concise but informative (2-3 paragraphs recommended)

#### Place Files in the `/assets` Folder
1. Copy your `linkedin.pdf` file to the `/assets` directory
2. Copy your `summary.txt` file to the `/assets` directory

Your file structure should look like:
```
/assets
├── linkedin.pdf
└── summary.txt
```

### 2. Local Development

#### Install Dependencies
```bash
# Install using uv (recommended)
uv sync
```

#### Run the Gradio App Locally
```bash
# Using uv
uv run linkedin_profile_chatbit/app.py
```

The Gradio interface will start on `http://localhost:7860` by default.

### 3. Deployment to Hugging Face Spaces

#### Prerequisites
- A Hugging Face account
- Your repository pushed to GitHub or Hugging Face Hub

#### Deploy to Hugging Face Spaces
1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose a name for your space
4. Select "Docker" as the SDK
5. Connect your GitHub repository or upload your files
6. The space will automatically build using the provided Dockerfile

#### Configuration
The project is pre-configured for Hugging Face Spaces with:
- **Dockerfile**: Uses Python 3.12 with uv for fast dependency management
- **README.md header**: Configured for Docker deployment
- **Port 7860**: Standard Gradio port for Hugging Face Spaces

### 4. Environment Variables

Create a `.env` file in your project root with your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

For Hugging Face Spaces, add this as a secret in your Space settings.

## Usage

### Local Usage
1. Run the application locally using `uv run run_gradio.py`
2. Open your browser to `http://localhost:7860`
3. Start chatting with your LinkedIn profile chatbot

### Deployed Usage
1. Once deployed to Hugging Face Spaces, your chatbot will be available at your Space URL
2. Share the URL with others or embed it in your website
3. The chatbot will answer questions about your professional background using your LinkedIn PDF and summary

## Features

- **Gradio Interface**: Clean, user-friendly chat interface
- **AI-Powered**: Uses OpenAI's GPT models for intelligent responses
- **Document Processing**: Extracts information from your LinkedIn PDF
- **Docker Deployment**: Containerized for reliable deployment
- **Fast Dependencies**: Uses uv for quick installation and updates
- **Responsive Design**: Works on desktop and mobile devices

## Technical Details

### Architecture
- **Frontend**: Gradio web interface
- **Backend**: Python with OpenAI API integration
- **Document Processing**: PyPDF for PDF text extraction
- **Deployment**: Docker container with Python 3.12
- **Dependency Management**: uv for fast, reliable package management

### Key Files
- `run_gradio.py`: Main entry point for the Gradio application
- `linkedin_profile_chatbot/app.py`: Gradio interface configuration
- `linkedin_profile_chatbot/chat.py`: Chat logic and AI integration
- `linkedin_profile_chatbot/core.py`: Core functionality and document processing
- `Dockerfile`: Container configuration for deployment
- `pyproject.toml`: Project configuration and dependencies

## Troubleshooting

### Common Issues

**Build fails on Hugging Face**: 
- Ensure your `.env` file is not committed to the repository
- Add your OpenAI API key as a secret in Hugging Face Spaces settings
- Check that all required files are present in the `/assets` folder

**Chatbot gives generic responses**: 
- Verify your `linkedin.pdf` and `summary.txt` files are in the `/assets` folder
- Check that the PDF contains readable text (not just images)
- Ensure your OpenAI API key is valid and has sufficient credits

**Local development issues**:
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Run `uv sync` to install dependencies
- Check that Python 3.12+ is available

### Docker Build Issues
If you encounter Docker build issues locally:
```bash
# Build the Docker image
docker build -t linkedin-chatbot .

# Run the container
docker run -p 7860:7860 linkedin-chatbot
```

## Support

For issues or questions:
1. Check the Hugging Face Spaces logs for deployment issues
2. Verify your OpenAI API key and credits
3. Ensure your profile documents are properly formatted and placed in `/assets`
