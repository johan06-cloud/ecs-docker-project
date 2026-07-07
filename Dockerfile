# Use a small, official Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list first (better Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Flask app listens on port 5000
EXPOSE 5000

# Use gunicorn (production WSGI server) instead of Flask's dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]