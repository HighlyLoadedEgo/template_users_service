from fastapi import FastAPI
from prometheus_client import make_asgi_app


def init_metrics(app: FastAPI) -> None:
    """Initialize the metric app for the application."""
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
