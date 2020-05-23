FROM python:3.7-alphine

RUN adduser -D blocksmurfer

WORKDIR /home/blocksmurfer

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY blocksmurfer blocksmurfer
COPY blocksmurfer.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP blocksmurfer.py

RUN chown -R blocksmurfer:blocksmurfer ./
USER blocksmurfer

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
