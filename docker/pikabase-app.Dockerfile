FROM python:3.8
RUN python -m pip install --upgrade pip
CMD gunicorn -b 0.0.0.0:8080 project.wsgi
WORKDIR /opt/pikabase
COPY manage.py manage.py
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY project project
COPY apps apps
