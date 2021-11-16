from typing import List
from fastapi import Depends, HTTPException
import ssl
import motor.motor_asyncio

uriString = 'mongodb://mongodb0.example.com:27017,mongodb1.example.com:27017/?replicaSet=myRepl'

def client_obj():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017/poc_db_23??replicaSet=myRepl&retryWrites=false&authSource=admin&socketTimeoutMS=60000&ssl=false")

    return client


async def get_db():
    client = client_obj()
    try:
        db = client.poc_db_23
        yield db
    finally:
        client.close()


async def coro(session):
  print("inside corrrrooooooooo")
  orders = session.client.db.orders
  inventory = session.client.db.inventory
  inserted_id = await orders.insert_one(
      {"sku": "abc123", "qty": 100}, session=session)
  await inventory.update_one(
      {"sku": "abc123", "qty": {"$gte": 100}},
      {"$inc": {"qty": -100}}, session=session)
  return inserted_id

async def create():
    print("******************************************")
    client = client_obj()
    # try:
    async with await client.start_session() as session:
      print("9999999999999999999999999999999999999999999")
      inserted_id = await session.with_transaction(coro)
    # except Exception as e:
    #     print("Exception---------------")
    return "success"

