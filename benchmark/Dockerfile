FROM docker:dind

WORKDIR /app

ENV WORKDIR=/workdir

COPY . /app

RUN apk add --no-cache python3 py3-pip bash curl ca-certificates \
  && pip3 install --no-cache-dir --break-system-packages --upgrade pip setuptools wheel

RUN pip3 install --no-cache-dir --break-system-packages -r /app/benchmark/requirements.txt

ENTRYPOINT ["sh", "-c", "/usr/local/bin/dockerd-entrypoint.sh & sleep 5 && python3 ./benchmark/benchmark.py"]
