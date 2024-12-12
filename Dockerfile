# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the current application code to the container
COPY . /app/

# Expose the port your app runs on
EXPOSE 5000

# Set the environment variable for the Flask app
ENV FLASK_APP=app.py

# Command to run the application
CMD ["bash", "-c", "python init_db.py && flask run --host=0.0.0.0"]