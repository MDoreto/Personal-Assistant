# pull official base image
FROM python:3.9

WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD ["gunicorn", "-b","0.0.0.0:5000", "-w 3","application:app"]