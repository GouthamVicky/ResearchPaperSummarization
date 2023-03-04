FROM python:3.8

# Copy requirements file and install dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Copy source code
COPY . /app/

# Set environment variables
ENV KAFKA_BOOTSTRAP_SERVERS=localhost:9092
ENV KAFKA_GROUP_ID=python-consumer

# Run the consumer script
CMD ["python", "consumerkafka.py"]