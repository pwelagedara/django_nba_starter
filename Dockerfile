FROM python:3.9.1-slim

# Copy the files
ADD . /app

# Set work directory
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


