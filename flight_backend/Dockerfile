# Use a Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the Django project files (if needed)
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run Celery (This will be overridden by docker-compose)
CMD ["celery", "-A", "flight_backend", "worker", "--loglevel=info"]
