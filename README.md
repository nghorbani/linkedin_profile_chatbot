# LinkedIn Profile Chatbot

A chatbot that can answer questions about your LinkedIn profile using AI. Upload your LinkedIn profile PDF and a summary, then deploy as a web service that can be embedded in any webpage.

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

#### Place Files in the `/me` Folder
1. Copy your `linkedin.pdf` file to the `/me` directory
2. Copy your `summary.txt` file to the `/me` directory

Your file structure should look like:
```
/me
├── linkedin.pdf
└── summary.txt
```

### 2. Local Development

#### Install Dependencies
```bash
# Install using uv (recommended)
uv sync

```

#### Run the Server Locally
```bash
python main.py
```

The server will start on `http://localhost:8000` by default.

### 3. Deployment with Render

#### Deploy to Render
1. Push your code to a GitHub repository
2. Go to [Render.com](https://render.com) and sign up/login
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure the deployment:
   - **Build Command**: `uv sync`
   - **Start Command**: `uvicorn main:app --host=0.0.0.0 --port=$PORT`
   - **Environment**: Python 3.11.10
6. Add any required environment variables
7. Click "Deploy Web Service"

Render will provide you with a public URL for your deployed chatbot API.

### 4. Embed in Your Webpage

#### Basic HTML Embedding
Add this HTML code to your webpage where you want the chat interface to appear:

```html
<div id="linkedin-chatbot">
    <iframe 
        src="https://your-render-app-name.onrender.com" 
        width="400" 
        height="600" 
        frameborder="0"
        style="border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
    </iframe>
</div>
```

#### Advanced Integration
For more control, you can integrate the chatbot using JavaScript:

```html
<div id="chatbot-container"></div>

<script>
// Create chatbot iframe dynamically
const chatbotContainer = document.getElementById('chatbot-container');
const iframe = document.createElement('iframe');
iframe.src = 'https://your-render-app-name.onrender.com';
iframe.width = '400';
iframe.height = '600';
iframe.style.border = 'none';
iframe.style.borderRadius = '10px';
iframe.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
chatbotContainer.appendChild(iframe);
</script>
```

#### Responsive Design
For mobile-friendly integration:

```css
#linkedin-chatbot iframe {
    width: 100%;
    max-width: 400px;
    height: 600px;
    border: none;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
    #linkedin-chatbot iframe {
        height: 500px;
    }
}
```

## Usage

Once deployed and embedded:

1. Visitors to your website can interact with the chatbot
2. The chatbot will answer questions about your professional background
3. It uses your LinkedIn PDF and summary to provide accurate, personalized responses
4. The chat interface is responsive and works on desktop and mobile devices

## Features

- AI-powered responses based on your LinkedIn profile
- Easy deployment with Render
- Embeddable in any webpage
- Responsive design
- Secure and private - your data stays in your deployment

## Troubleshooting

### Common Issues

**Chatbot not loading**: Check that your Render deployment is active and the URL is correct.

**No responses**: Ensure your `linkedin.pdf` and `summary.txt` files are properly placed in the `/me` folder.

**Deployment fails**: Check the Render logs for specific error messages and ensure all dependencies are properly listed.

## Support

For issues or questions, please check the deployment logs on Render or review the local server output for debugging information.
