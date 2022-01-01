FROM python:3.10.0-slim

RUN useradd -ms /bin/bash blocksmurfer
WORKDIR /home/blocksmurfer

RUN apt-get update && apt-get install -y \
  build-essential \
  python-dev \
  python3-dev \
  libgmp3-dev \
  libssl-dev

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY blocksmurfer blocksmurfer
COPY blocksmurfer.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP blocksmurfer.py

RUN chown -R blocksmurfer:blocksmurfer ./
USER blocksmurfer

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
