FROM python:3.9

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy the main script
COPY main.py /app/main.py

# Set the working directory
WORKDIR /app

# Start the script
CMD ["python3", "main.py"]