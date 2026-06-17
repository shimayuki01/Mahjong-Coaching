
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    libboost-all-dev \
    python3 \
    python3-pip

WORKDIR /app
COPY akochan/ /app/akochan/

WORKDIR /app/akochan/ai_src
RUN make -f Makefile_Linux

WORKDIR /app/akochan
RUN make -f Makefile_Linux

ENV LD_LIBRARY_PATH=/app/akochan/ai_src:$LD_LIBRARY_PATH

CMD ["/bin/bash"]


# # ローカルの akochan ディレクトリを丸ごとコピー


# # Python 依存をインストール
# # RUN pip install --no-cache-dir -r requirements.txt

