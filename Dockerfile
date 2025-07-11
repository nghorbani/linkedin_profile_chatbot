FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    rsync \
    libgl1-mesa-glx \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /code

# Copy uv configuration files and package directory
COPY pyproject.toml uv.lock ./
COPY linkedin_profile_chatbot/ ./linkedin_profile_chatbot/

# Set a fallback version for setuptools-scm
ENV SETUPTOOLS_SCM_PRETEND_VERSION=1.0.0

# Install dependencies using uv
RUN uv sync --frozen --no-cache

# Copy the rest of the application
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONPATH=/code

# Set the working directory to user's home
WORKDIR $HOME/app

# Copy the application as the user
COPY --chown=user . $HOME/app

# Expose the port that Gradio will run on
EXPOSE 7860

# Set environment variables for Gradio
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT="7860"

# Command to run the application using uv
CMD ["uv", "run", "run_gradio.py"]
