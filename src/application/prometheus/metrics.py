from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Summary,
)

from src.application.prometheus.constants import LabelNames

# Counter for counting the number of requests
request_count = Counter(
    "request_count",
    "Total request count",
    [LabelNames.METHOD.value, LabelNames.PATH.value, LabelNames.STATUS.value],
)
# Histogram for measuring request processing time
request_time = Histogram(
    "request_time",
    "Request time",
    [LabelNames.METHOD.value, LabelNames.PATH.value, LabelNames.STATUS.value],
)
# Cumulative metric for measuring request processing time (alternative to histogram)
request_summary = Summary(
    "request_summary",
    "Request summary",
    [LabelNames.METHOD.value, LabelNames.PATH.value, LabelNames.STATUS.value],
)
# Label for displaying the current number of active requests
request_in_progress = Gauge(
    "request_in_progress",
    "Requests in progress",
    [LabelNames.METHOD.value, LabelNames.PATH.value],
)
