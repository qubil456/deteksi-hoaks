# Dockerfile for Streamlit hoax-detection app
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only requirements first for layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . /app

# Expose Streamlit default port
EXPOSE 8501

# Run streamlit in headless mode
CMD ["python", "-m", "streamlit", "run", "Script/app.py", "--server.headless", "true", "--server.port", "8501"]
