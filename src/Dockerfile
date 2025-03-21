FROM python:3.8-slim-buster

WORKDIR /src

# Install dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "sh", "-c", "sleep 10 && python3 -m flask run --host=0.0.0.0" ]
