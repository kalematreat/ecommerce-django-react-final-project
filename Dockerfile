FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code

# Copy the requirements file and install backend dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the frontend part of the project
COPY frontend/package.json frontend/package-lock.json /frontend/

# Set working directory to frontend
WORKDIR /frontend

# Install frontend dependencies and build the project
RUN npm install
RUN npm run build

# Copy the rest of the project
WORKDIR /code
COPY . .

# Expose the port
EXPOSE 8000

# Set Django settings module
ENV DJANGO_SETTINGS_MODULE=background.settings

# Run the application with gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
