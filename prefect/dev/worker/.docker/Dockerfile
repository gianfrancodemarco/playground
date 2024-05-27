FROM prefecthq/prefect:2.19.1-python3.10

COPY flows /flows
COPY requirements.txt /flows
COPY prefect.yaml /flows
RUN pip install -r /flows/requirements.txt
