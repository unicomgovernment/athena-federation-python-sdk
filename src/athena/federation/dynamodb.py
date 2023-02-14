import os

import pyarrow

from athena.federation.athena_data_source import AthenaDataSource
from athena.federation.lambda_handler import AthenaLambdaHandler
from lib.logging import logger

SPILL_BUCKET = os.environ.get("SPILL_BUCKET")


class DynamoDataSource(AthenaDataSource):
    """Athena Data Source for DynamoDB. Somewhat converted from AWS' Java 8 implementation.
    See https://github.com/awslabs/aws-athena-query-federation/tree/master/athena-dynamodb"""

    def __init__(self):
        super().__init__()

    def databases(self) -> list[str]:
        pass

    def tables(self, database_name: str) -> list[str]:
        pass

    def schema(self, database_name: str, table_name: str) -> pyarrow.Schema:
        pass

    def records(self, database_name: str, table_name: str, split):
        pass


DATA_SOURCE = DynamoDataSource()
HANDLER = AthenaLambdaHandler(DATA_SOURCE, SPILL_BUCKET)


def lambda_handler(event, context):
    logger.debug(f"Event: {event}")

    return HANDLER.process_event(event)
