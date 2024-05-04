FROM python:3.8 
 
# Install any necessary dependencies 
RUN pip install boto3 
# Copy Python script into the container 
COPY helloworld.py /app/helloworld.py 
# Set the working directory 
WORKDIR /app 
# Run the Python script when the container starts 
CMD ["python", "helloworld.py"] 
