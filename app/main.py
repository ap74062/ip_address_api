from fastapi import FastAPI
from database import Database
from cache import Cache
from api import IPStackApi
from utils import assert_corect_api_result

# Could be moved to .env file for better security
# But for testing purposes I leave it here
REDIS_HOST = "redis"
REDIS_PORT = "6379"
REDIS_DB = "data"
MONGODB_HOST = "mongodb"
MONGODB_PORT = 27017
MONGODB_DB = "data"
MONGODB_COLLECTION = "data"
API_ACCESS_KEY = "0f166172ea082c6e68d938fb770813d1"


def db_connector():
    db = Database(
        host=MONGODB_HOST,
        port=MONGODB_PORT,
        db=MONGODB_DB,
        collection=MONGODB_COLLECTION
    )
    return db


def cache_connector():
    cache = Cache(
        host=REDIS_HOST,
        port=REDIS_PORT,
    )
    return cache


def api_connector():
    api = IPStackApi(api_access_key=API_ACCESS_KEY)
    return api


app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db = db_connector()
    app.cache = cache_connector()
    app.api = api_connector()


@app.on_event("shutdown")
async def shutdown():
    app.db.close()
    # redis db (cache) uses connection pool so don't need to be closed


@app.get('/get_address/{ip_address}')
async def get_address(ip_address: str) -> dict:
    cache_address = app.cache.get(ip_address)
    if cache_address:
        return cache_address

    db_address = app.db.get_row(ip_address)
    if db_address:
        return db_address

    api_address = app.api.get(ip_address)
    if assert_corect_api_result(api_address):
        app.cache.set(ip_address, api_address)
        app.db.add_row(ip_address, api_address)

    return api_address
