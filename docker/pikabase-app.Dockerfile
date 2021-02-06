FROM python:3.8
RUN python -m pip install --upgrade pip
WORKDIR /opt/pikabase
CMD python run.py
COPY manage.py manage.py
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.py run.py
COPY project project
COPY apps apps
