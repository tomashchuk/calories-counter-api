FROM nickgryg/alpine-pandas
#FROM python:3.10-alpine
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev zlib-dev

# RUN apt-y update && apt install -y libzbar-dev

# install dependencies
COPY requirements.txt /app/requirements.txt
COPY requirements.txt /app/test/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt -r test/requirements.txt


# copy project
COPY . .

#port from the container to expose to host
EXPOSE 8000

CMD /app/start.sh