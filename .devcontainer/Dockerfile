# Use the official Python 3.11 image based on Debian
FROM ubuntu:jammy

# # Install necessary system dependencies for Python and general tools using apt-get
RUN apt-get update && apt-get install -y \
    build-essential \
    bash \
    python3 \
    python3-pip \
    curl \
    git \
    sudo \
    # Cleans up temporary files created by apt-get
    && rm -rf /var/lib/apt/lists/*

# Install some Python 3 tools
RUN pip3 install --upgrade pip \
    && pip3 install virtualenv

# Add a non-root user and set permissions
RUN useradd -m -s /bin/bash devuser \
    && echo "devuser:devuser" | chpasswd \
    && adduser devuser sudo

# Set a working directory for the container
WORKDIR /workspace
