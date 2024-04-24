FROM python:3.11-slim

# Display the Python output through the terminal
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Add Python dependencies
## Update pip
RUN pip install --upgrade pip

## Install build tools
RUN apt-get update && apt-get install -y build-essential

## Copy requirements
COPY requirements.txt ./requirements.txt

## Install requirements
RUN pip install -r requirements.txt
