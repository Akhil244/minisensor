# Use Python 3.12.4 slim image
FROM python:3.12.4-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (gcc is often needed for building some Python packages)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy project files to /app
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install setup.py (if it installs your package)
RUN python setup.py install

# Install pip requirements
RUN pip install -r requirements.txt

# Install latest python-multipart
RUN pip install --upgrade python-multipart

# Set environment variable placeholder (can override at runtime)
ENV MONGO_DB_URL=""

# Render sets PORT dynamically, so don’t hardcode 80
EXPOSE 8000

# Run the app with Uvicorn, binding to 0.0.0.0 and Render's PORT
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
