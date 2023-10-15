# Use an official Python runtime as a parent image
FROM python:3.11

# Set working directory
WORKDIR /app

# Set up venv   
RUN python -m venv .venv
ENV PATH="./.venv/bin:$PATH"


# Install Nginx
RUN apt-get update && apt-get install -y nginx supervisor

# Copy requirements and install Python dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy Nginx config file
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Copy supervisor config file
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy the current directory contents into the container
COPY . .

# Run supervisord
CMD ["/usr/bin/supervisord"]

EXPOSE 80


