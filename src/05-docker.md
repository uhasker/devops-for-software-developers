# Docker

Docker is for **containerization**, i.e. packaging an application together with its dependencies as an image and running it as a container.

## Example

Example Dockerfile:

```
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Define the command to run the application
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

Example `docker-compose.yml`:

```yml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - FLASK_APP=app.py
      - SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@db:5432/taskdb

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: taskdb
    ports:
      - "5432:5432"
```
