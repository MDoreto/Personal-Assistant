FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
ENV DIALOGFLOW_PROJECT_ID=jarvis-sqri
ENV GOOGLE_APPLICATION_CREDENTIALS=jarvis-sqri-db7648fb066e.json
COPY --from=mwader/static-ffmpeg:4.1.4-2 /ffmpeg /ffprobe /usr/local/bin/
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app