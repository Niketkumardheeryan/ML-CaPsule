# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install python development & helper packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    notebook \
    black[jupyter] \
    flake8

# Copy requirements.txt and install dependencies
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports: 8888 for Jupyter Notebook, 8501 for Streamlit
EXPOSE 8888 8501

# Run Jupyter Notebook by default
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
