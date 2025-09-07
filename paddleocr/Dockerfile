FROM python:3.8.18-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -i https://www.paddlepaddle.org.cn/packages/stable/cpu/ paddlepaddle==2.6.2
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
    click \
    fastapi \
    uvicorn \
    chardet \
    pandas \
    openpyxl \
    numpy \
    protobuf \
    pillow \
    PyYAML \
    python-multipart \
    scikit-image \
    scikit-learn \
    scipy \
    pycocotools \
    shapely \
    Polygon3 \
    requests \
    tqdm \
    pyclipper \
    opencv-python-headless \
    paddle-bfloat \
    PyMuPDF==1.24.7 \
    PyMuPDFb==1.24.6

WORKDIR /workspace

COPY . .

CMD ["python", "main.py"]
