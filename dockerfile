# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for Prometheus metrics
EXPOSE 8000

# Ensure the log file is writable
RUN touch eth_deposit_tracker.log && chmod 666 eth_deposit_tracker.log

# Run the main.py when the container launches
CMD ["python", "main.py"]