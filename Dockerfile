FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Copy the backend requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the entire backend code
COPY . .

# Set up the frontend build
WORKDIR /code/frontend
RUN npm install
RUN npm run build

# Expose the application port
EXPOSE 8000

# Set the Django settings module
ENV DJANGO_SETTINGS_MODULE=background.settings

# Run the application using gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
