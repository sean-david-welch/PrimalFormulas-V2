# Use the official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Install requirements
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy local code to the container
COPY . .

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
