# Start with the base image of python:3.9-alpine
FROM ubuntu:jammy-20230126


RUN apt-get update && apt-get install -y python3 python3-pip 
# Copy the script and required files to the /app directory
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install the required dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Run the collect_data.py script
CMD ["python3", "collect-remote.py"]
