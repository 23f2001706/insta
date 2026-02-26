FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8000

# Run the app
CMD ["gunicorn", "--workers", "4", "--worker-class", "sync", "--bind", "0.0.0.0:8000", "app:app"]
