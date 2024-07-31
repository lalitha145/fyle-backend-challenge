# Use the official Python image.
FROM python:3.8-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file into the container.
COPY core/requirements.txt ./

# Install the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container.
COPY core/ /app/

# Expose port 5000 for the Flask application.
EXPOSE 5000

# Run the Flask application.
CMD ["flask", "run", "--host=0.0.0.0"]
