FROM python:3.10

RUN pip install pandas

WORKDIR /the/checking/
COPY pipeling.py pipeline_docker.py

ENTRYPOINT ["python","pipeline_docker.py"]