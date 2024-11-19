FROM python:3.11-slim

RUN useradd -ms /bin/bash blocksmurfer
WORKDIR /home/blocksmurfer

RUN apt-get update && apt-get install -y \
  build-essential \
  python3-dev \
  libgmp3-dev \
  libssl-dev

COPY requirements.txt requirements.txt
RUN python3 -m venv venv/blocksmurfer
RUN venv/blocksmurfer/bin/pip3 install -r requirements.txt

COPY blocksmurfer blocksmurfer
COPY app.py config.py boot.sh ./
RUN chmod +x boot.sh

RUN chown -R blocksmurfer:blocksmurfer ./
USER blocksmurfer

EXPOSE 5000
#ENTRYPOINT ["./boot.sh"]
ENTRYPOINT ["./venv/blocksmurfer/bin/flask", "run", "--host", "0.0.0.0"]
