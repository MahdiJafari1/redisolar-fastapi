import os

from fastapi import FastAPI
from redis import exceptions

from redisolar.api.capacity import CapacityReportResource
from redisolar.api.meter_reading import (
    GlobalMeterReadingResource,
    SiteMeterReadingResource,
)
from redisolar.api.metrics import MetricsResource
from redisolar.api.site import SiteListResource, SiteResource
from redisolar.api.site_geo import SiteGeoListResource, SiteGeoResource
from redisolar.core.connections import get_redis_connection
from redisolar.dao.redis import (
    CapacityReportDaoRedis,
    FeedDaoRedis,
    MeterReadingDaoRedis,
    MetricDaoRedis,
    SiteDaoRedis,
    SiteGeoDaoRedis,
)
from redisolar.dao.redis.key_schema import KeySchema

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    key_schema = KeySchema(os.environ["REDIS_KEY_PREFIX"])
    redis_client = get_redis_connection(
        os.environ["REDIS_HOST"], os.environ["REDIS_PORT"]
    )
    try:
        await redis_client.ping()
    except exceptions.ConnectionError:
        raise RuntimeError(
            "Redis authentication failed. Make sure you set "
            "$REDISOLAR_REDIS_PASSWORD to the correct password "
            "for your Redis instance. Stopping server."
        )

    if os.environ.get("USE_GEO_SITE_API"):
        app.include_router(
            SiteGeoListResource(
                redis_client=redis_client, key_schema=key_schema
            ).router,
            prefix="/sites",
        )
        app.include_router(
            SiteGeoResource(redis_client=redis_client, key_schema=key_schema).router,
            prefix="/sites",
        )
    else:
        app.include_router(
            SiteListResource(redis_client=redis_client, key_schema=key_schema).router,
            prefix="/sites",
        )
        app.include_router(
            SiteResource(redis_client=redis_client, key_schema=key_schema).router,
            prefix="/sites",
        )
    app.include_router(
        CapacityReportResource(redis_client=redis_client, key_schema=key_schema).router,
        prefix="/capacity",
    )
    app.include_router(
        GlobalMeterReadingResource(
            redis_client=redis_client,
            key_schema=key_schema,
            feed_dao=FeedDaoRedis(redis_client, key_schema),
        ).router,
        prefix="/meter_readings",
    )
    app.include_router(
        SiteMeterReadingResource(
            redis_client=redis_client,
            key_schema=key_schema,
            feed_dao=FeedDaoRedis(redis_client, key_schema),
        ).router,
        prefix="/meter_readings",
    )
    app.include_router(
        MetricsResource(redis_client=redis_client, key_schema=key_schema).router,
        prefix="/metrics",
    )
