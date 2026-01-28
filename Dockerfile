
# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Install system dependencies (required for some python packages like rembg generally, though u2netp is lighter)
# git is often needed for installing dependencies from git
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code

# Create a writable directory for uploads (Hugging Face Spaces runs as user 1000 usually)
RUN mkdir -p /code/static/uploads && chmod 777 /code/static/uploads
RUN mkdir -p /code/.u2net && chmod 777 /code/.u2net

# Set home for rembg to find models in a writable place
ENV U2NET_HOME=/code/.u2net

# Expose the port (Hugging Face Spaces expects 7860 by default)
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
