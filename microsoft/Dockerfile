FROM ubuntu:22.04

ENV PIP_NO_CACHE_DIR=off

RUN apt-get update && apt-get install -y \
    python3-pip \
    libaio1 \
    libnsl2 && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install \
    loguru \
    fastapi \
    uvicorn \
    langchain_community \
    python-multipart \
    unstructured \
    python-docx \
    docx2txt \
    pdfminer.six

WORKDIR /workspace

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--access-log"]
