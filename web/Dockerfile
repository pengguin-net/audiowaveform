FROM python:3.10-slim
ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
RUN apt-get update -y && apt-get install libmad0-dev \
      libid3tag0-dev libsndfile1-dev libgd-dev libboost-filesystem-dev \
      libboost-program-options-dev \
      libboost-regex-dev -y
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY src ./

EXPOSE 8080
CMD exec gunicorn -w1 --bind 0.0.0.0:8080 app:app