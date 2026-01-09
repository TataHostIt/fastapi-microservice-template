# Use the official lightweight Python 3.11 image
FROM harbor.tatahostit.com/dockerhub/python:3.11-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to the root of the project
WORKDIR /code

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the start script is executable
RUN chmod +x start.sh

# Expose the port (Gunicorn default usually 8000, adjust if your config differs)
EXPOSE 8080

# Run the start script
CMD ["./start.sh"]