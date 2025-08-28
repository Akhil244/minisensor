# Use Python 3.12.4 slim image
FROM python:3.12.4-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (gcc is often needed for some Python packages)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy everything from repo (including model.pkl and main.py)
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# (Optional) Install latest python-multipart if needed by FastAPI
RUN pip install --upgrade python-multipart

# Expose port (Render dynamically assigns PORT, default 8000)
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
