###########
# BUILDER #
###########

FROM python:3.8 as builder

WORKDIR /usr/src/lbs_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY . .
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/lbs_backend/wheels -r requirements.txt


#########
# FINAL #
#########

FROM python:3.8

RUN mkdir -p /home/lbs_backend

RUN groupadd lbs_backend && useradd -g lbs_backend lbs_backend

ENV HOME=/home/lbs_backend
ENV APP_HOME=/home/lbs_backend/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

RUN apt-get update
COPY --from=builder /usr/src/lbs_backend/wheels /wheels
COPY --from=builder /usr/src/lbs_backend/requirements.txt .
RUN pip install --no-cache /wheels/*


COPY . $APP_HOME

RUN chown -R lbs_backend:lbs_backend $APP_HOME

USER lbs_backend

