brew install python@3.12
python3 -m pip install -r prefect/app/requirements.txt
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect work-pool create test-pool process
prefect deploy --prefect-file prefect/dev/worker/.docker/prefect.yaml

In the server pod:
cd /flows
prefect deploy --all