FROM python:3.12.3-bullseye

# Checkout and install dagster libraries needed to run the gRPC server
# exposing your repository to dagster-webserver and dagster-daemon, and to load the DagsterInstance

RUN pip install \
    dagster \
    dagster-postgres \
    dagster-docker

# Add repository code

WORKDIR /opt/dagster/app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY fitster/ .

# Run dagster gRPC server on port 4000
EXPOSE 4000

CMD ["dagster", "code-server", "start", "-h", "0.0.0.0", "-p", "3030", "-m", "fitster"]