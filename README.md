# (Unofficial) Python SDK for Athena Federation

This is an _unofficial_ Python SDK for Athena Federation.

## Overview

The Python SDK makes it easy to create new Amazon Athena Data Source Connectors using Python. It is under active development so the API may change from version to version.

You can see an example implementation that [queries Google Sheets using Athena](https://github.com/dacort/athena-gsheets).

![gsheets_example](https://user-images.githubusercontent.com/1512/134044216-f8498ce8-2015-4935-bc95-6f9fd5234a25.png)

### Current Limitations

- Partitions are not supported, so Athena will not parallelize the query using partitions.

## Local Development

- Ensure you've got the `build` module install and SDK dependencies.

```
pip install build
pip install -r requirements.txt
```

- Now make a wheel.

```shell
python -m build
```

This will create a file in `dist/`: `dist/unoffical_athena_federation_sdk-0.0.0-py3-none-any.whl`

Copy that file to your example repo and you can include it in your `requirements.txt` like so:

```
unoffical-athena-federation-sdk @ file:///unoffical_athena_federation_sdk-0.0.0-py3-none-any.whl
```

## Validating your connector

You can test your Lambda function locally using Lambda Docker images.

First, build our Docker image and run it.

```shell
docker build -t local/athena-python-example .
docker run --rm -p 9000:8080 local/athena-python-example
```

Then, we can execute a sample `PingRequest`.

```shell
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"@type": "PingRequest", "identity": {"id": "UNKNOWN", "principal": "UNKNOWN", "account": "123456789012", "arn": "arn:aws:iam::123456789012:root", "tags": {}, "groups": []}, "catalogName": "athena_python_sdk", "queryId": "1681559a-548b-4771-874c-2aa2ea7c39ab"}'
```

```json
{"@type": "PingResponse", "catalogName": "athena_python_sdk", "queryId": "1681559a-548b-4771-874c-2aa2ea7c39ab", "sourceType": "athena_python_sdk", "capabilities": 23}
```

We can also list schemas.

```shell
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"@type": "ListSchemasRequest", "identity": {"id": "UNKNOWN", "principal": "UNKNOWN", "account": "123456789012", "arn": "arn:aws:iam::123456789012:root", "tags": {}, "groups": []}, "catalogName": "athena_python_sdk", "queryId": "1681559a-548b-4771-874c-2aa2ea7c39ab"}'
```

```json
{"@type": "ListSchemasResponse", "catalogName": "athena_python_sdk", "schemas": ["sampledb"], "requestType": "LIST_SCHEMAS"}
```
