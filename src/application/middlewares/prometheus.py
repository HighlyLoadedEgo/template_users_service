import time

from fastapi import Request

from src.application.prometheus.metrics import (
    request_count,
    request_in_progress,
    request_summary,
    request_time,
)


async def prometheus_metrics_middleware(request: Request, call_next):
    start_time = time.time()
    request_in_progress.labels(request.method, request.url.path).inc()

    response = await call_next(request)

    request_in_progress.labels(request.method, request.url.path).dec()
    end_time = time.time()
    request_count.labels(request.method, request.url.path, response.status_code).inc()
    request_time.labels(request.method, request.url.path, response.status_code).observe(
        end_time - start_time
    )
    request_summary.labels(
        request.method, request.url.path, response.status_code
    ).observe(end_time - start_time)

    return response
