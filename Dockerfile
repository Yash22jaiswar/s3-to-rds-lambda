# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and requirements file into the container at /app
COPY data_transfer.py ./
COPY requirements.txt ./

# Install any needed dependencies specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run the Python script when the container launches
CMD ["python", "./data_transfer.py"]
