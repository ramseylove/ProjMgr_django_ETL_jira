# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /code

# Install dependencies
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --deploy --system

# Copy project
COPY . /code/

################  Start New Image  :  Debugger  ############
# FROM base as debug
# RUN pipenv install ptvsd

# WORKDIR /code/
# CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess manage.py runserver 127.0.0.1:8000