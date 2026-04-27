# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for MySQL connector
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# --- Security & Environment Configuration ---
# These ARGs allow GitHub Actions to pass secrets during the build process
ARG DB_PASSWORD
ARG FLASK_SECRET

# These ENVs make the secrets available to your Python app at runtime
ENV DB_PASSWORD=$DB_PASSWORD
ENV FLASK_SECRET=$FLASK_SECRET
# --------------------------------------------

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
