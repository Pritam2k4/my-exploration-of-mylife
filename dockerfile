# Use a lightweight Linux base image
FROM ubuntu:22.04

# Set working directory inside container
WORKDIR /repo

# Copy all repository contents
COPY . .

# Install basic utilities (customize if needed)
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Default command (interactive shell)
CMD ["bash"]docker build -t my-exploration-of-mylife .

