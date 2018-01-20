FROM python:3
WORKDIR /usr/src/cryptopals
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
VOLUME /usr/src/cryptopals
