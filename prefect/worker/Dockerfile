FROM python:3.12-slim

WORKDIR /app

COPY flows /flows
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run Prefect server when the container launches
CMD ["prefect", "worker", "start"]