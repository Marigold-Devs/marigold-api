FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NOWARNINGS="yes"

RUN apt-get update
RUN apt-get install -y gcc python3.8 python3.8-dev python3-pip default-libmysqlclient-dev apt-utils libpango1.0-0 libcairo2 libpq-dev

# Use python3.8 instead of 3.6
RUN : \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3.8-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :
RUN python3.8 -m venv /venv
ENV PATH=/venv/bin:$PATH

# Install pip and poetry
RUN pip3 install -U pip
RUN pip3 install poetry==1.1.13

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install python packages via pip
COPY pyproject.toml pyproject.toml
RUN poetry config virtualenvs.create false \
 && poetry install --no-dev --no-interaction --no-ansi

COPY backend backend
COPY manage.py manage.py

# collect static
RUN mkdir /app/static
RUN python3 manage.py collectstatic --noinput --clear

EXPOSE $PORT

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 backend.wsgi:application