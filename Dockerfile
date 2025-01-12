FROM python:3
RUN pip install requests
WORKDIR /code
COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY backend/ . 
CMD ["python", "manage.py", "runserver"]

