FROM python:3.9-slim-buster  

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port (same as the Flask app runs on by default)
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]