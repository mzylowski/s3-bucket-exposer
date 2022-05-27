FROM python:3.10.2-slim-buster AS compiler

RUN apt clean \
    && apt update -y \
    && apt install nginx python3-dev build-essential --no-install-recommends -y

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY s3-bucket-exposer/requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM python:3.10.2-slim-buster AS app
COPY --from=compiler /opt/venv /opt/venv

RUN apt clean \
    && apt update -y \
    && apt install nginx --no-install-recommends -y \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt clean

COPY s3-bucket-exposer /srv/s3-bucket-exposer
COPY container/uwsgi.ini /srv/s3-bucket-exposer
COPY container/run.sh /srv/s3-bucket-exposer
WORKDIR /srv/s3-bucket-exposer

ARG FLASK_ENV="production"
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED="true"

COPY container/nginx.conf /etc/nginx
RUN chmod +x ./run.sh
CMD ["./run.sh"]
