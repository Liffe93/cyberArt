#use a lightweight python image suitable for Raspberry Pi 400 (ARM archietecture)
FROM python:3.11-slim-buster

#Set the working directory in the containter
WORKDIR /app

# Copy the current directory contents into the container at /app 
COPY . /app

# Install any needed packages secific in requirments.txt 
RUN pip install --no-cache-dir -r requirments.txt

# make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables 
ENV FLASK_APP=script.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app 
CMD ["flask", "run"]

