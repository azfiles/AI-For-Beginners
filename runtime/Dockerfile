FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends git curl ca-certificates build-essential libgomp1 default-jre-headless && rm -rf /var/lib/apt/lists/*
COPY site/requirements-learning.txt site/requirements-advanced.txt /opt/requirements/
RUN python -m pip install --no-cache-dir torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cpu
RUN python -m pip install --no-cache-dir -r /opt/requirements/requirements-advanced.txt 'jupyterlab>=4,<5'
RUN useradd --create-home --uid 1000 learner && mkdir -p /course /cache /opt/course && chown -R learner:learner /course /cache /opt/course
COPY --chown=learner:learner lessons /opt/course/lessons
COPY --chown=learner:learner examples /opt/course/examples
COPY --chown=learner:learner data /opt/course/data
COPY --chown=learner:learner site /opt/course/site
COPY runtime/start.py runtime/jupyter_server_config.py /opt/runtime/
ENV HOME=/home/learner HF_HOME=/cache/huggingface TORCH_HOME=/cache/torch KERAS_HOME=/cache/keras TFDS_DATA_DIR=/cache/tfds XDG_CACHE_HOME=/cache/xdg GENSIM_DATA_DIR=/cache/gensim
USER learner
WORKDIR /course
EXPOSE 8888
CMD ["python", "/opt/runtime/start.py"]
