FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
ENV DJANGO_SETTING_MODULE=background.settings
# CMD ["python", "manage.py","runserver"]
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]