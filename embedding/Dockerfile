FROM nvidia/cuda:12.8.0-cudnn-runtime-ubuntu22.04

ENV PIP_NO_CACHE_DIR=off

RUN apt-get update && apt-get install -y \
    python3-pip \
    libaio1 \
    libnsl2 && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --upgrade pip && \
    pip3 install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu128 && \
    pip install loguru fastapi uvicorn BCEmbedding==0.1.1

WORKDIR /workspace

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--access-log"]
