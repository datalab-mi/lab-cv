FROM ovhcom/ai-training-pytorch:1.8.1
LABEL maintainer="datalab-mi"

RUN apt update -y && \
    apt install -y bash \
                   build-essential \
                   g++ \
		   ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists

RUN mkdir /workspace && chown -R 42420:42420 /workspace
WORKDIR /workspace
COPY requirements.txt requirements.txt
COPY workspace/* ./
RUN pip install --no-cache-dir -r requirements.txt
