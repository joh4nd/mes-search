
FROM python:3.12-slim-bookworm

WORKDIR /app/src/pipeline

COPY data ../../data/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt
# RUN pip uninstall nvidia-nvtx-cu12 nvidia-nvjitlink-cu12  nvidia-nccl-cu12 nvidia-curand-cu12 nvidia-cufft-cu12 nvidia-cuda-runtime-cu12 nvidia-cuda-nvrtc-cu12 nvidia-cuda-cupti-cu12 nvidia-cublas-cu12 nvidia-cusparse-cu12 nvidia-cudnn-cu12 nvidia-cusolver-cu12

# prod
ENTRYPOINT python3 -m data-to-index

# dev
# ENTRYPOINT jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser
