import json
import logging
import os
from datetime import datetime

from lib.enumerations import MetricUnit

REGION = os.environ.get("AWS_REGION", "us-east-1")
LOG_LEVEL = int(os.environ.get("LOG_LEVEL", logging.INFO))
SERVICE_NAME = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "unknown_service")
NAMESPACE = os.environ.get("NAMESPACE", "multivac")

logger = logging.getLogger(NAMESPACE)
logger.setLevel(LOG_LEVEL)


def add_metric(name: str, unit: MetricUnit, value):
    """
    Embed system-wide and lambda-specific metrics to CloudWatch logs for later ingestion into CloudWatch metrics
    See: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html
    """

    timestamp = datetime.utcnow().timestamp()
    entry = {
        "_aws": {
            "Timestamp": int(timestamp * 1000),
            "CloudWatchMetrics": [
                {"Dimensions": [["service"]], "Namespace": NAMESPACE, "Metrics": [{"Name": name, "Unit": unit.value}]}
            ],
        },
        name: value,
    }

    logger.info(json.dumps({"service": SERVICE_NAME, **entry}, indent=2))
    logger.info(json.dumps({"service": "api", **entry}, indent=2))


XRAY_ENABLED = True
try:
    from aws_xray_sdk.core import patch_all

    patch_all()
except ImportError:
    patch_all = None
    XRAY_ENABLED = False
    logger.debug("X-Ray tracing is disabled.")


def log_lambda_metrics(event, context):
    logger.info(f"EVENT: {json.dumps(event, indent=2)}")

    if context:
        try:
            logger.info(f"Remaining time: {context.get_remaining_time_in_millis()}")
        except AttributeError as error:
            logger.exception(error)
