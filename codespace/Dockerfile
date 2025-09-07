FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libaio1 \
    libnsl2 \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

RUN pip install --no-cache-dir \
    jupyter \
    jupyterlab-language-pack-zh-CN \
    pandas \
    matplotlib \
    PyMySQL \
    cx_Oracle \
    DBUtils \
    xlrd \
    xlwt \
    cryptography

ENV ORACLE_HOME=/opt/oracle/instantclient_12_2
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME

RUN echo '#!/bin/sh' > /start.sh && \
    echo 'cd /workspace' >> /start.sh && \
    echo 'jupyter notebook --ip=0.0.0.0 --port=80 --no-browser --allow-root --notebook-dir=/workspace --ServerApp.base_url=${CODESPACE_BASE} --ServerApp.custom_display_url="http://${CODESPACE_HOST}:${CODESPACE_PORT}${CODESPACE_BASE}" --ServerApp.token='' --ServerApp.allow_origin='*' --ServerApp.allow_origin_pat='.*' --ServerApp.allow_remote_access=True --ServerApp.trust_xheaders=True --ServerApp.disable_check_xsrf=True --ServerApp.tornado_settings="{\"headers\":{\"Content-Security-Policy\":\"frame-ancestors self *\"}}"' >> /start.sh

RUN chmod +x /start.sh

WORKDIR /workspace

CMD ["/start.sh"]
