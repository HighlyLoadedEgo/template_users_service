from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream.rabbit import RabbitBroker


def get_lifespan(broker: RabbitBroker):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await broker.start()
        yield
        await broker.close()

    return lifespan
