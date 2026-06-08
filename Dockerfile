FROM mambaorg/micromamba:1.5.8

WORKDIR /app

COPY environment.yaml /tmp/environment.yaml

RUN micromamba install -y -n base -f /tmp/environment.yaml && \
    micromamba clean --all --yes

COPY . /app

EXPOSE 8501

CMD ["micromamba", "run", "-n", "base", "streamlit", "run", "cointoss_basicinput.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.baseUrlPath=cointoss-basic-input"]
