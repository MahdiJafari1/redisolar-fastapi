import redis
from redis.sentinel import Sentinel
from rediscluster import RedisCluster


def connection_examples():
    # connect to a standard Redis deployment
    client = redis.Redis(
        host="localhost", port=6379, decode_responses=True, max_connections=20
    )

    # Read and Write through the client
    client.set("foot", "bar")
    client.get("foo")

    #
