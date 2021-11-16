import motor.motor_asyncio
import asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017/test_db, mongodb://localhost:27017/test2_db")


# async def coro():
#     collection = client.db.collection

#     # End the session after using it.
#     s = await client.start_session()
#     await s.end_session()

#     # Or, use an "async with" statement to end the session
#     # automatically.
#     async with await client.start_session() as s:
#         doc = {'_id': ObjectId(), 'x': 1}
#         await collection.insert_one(doc, session=s)

#         secondary = collection.with_options(
#             read_preference=ReadPreference.SECONDARY)

#         # Sessions are causally consistent by default, so we can read
#         # the doc we just inserted, even reading from a secondary.
#         async for doc in secondary.find(session=s):
#             print(doc)

#     # Run a multi-document transaction:
#     async with await client.start_session() as s:
#         # Note, start_transaction doesn't require "await".
#         async with s.start_transaction():
#             await collection.delete_one({'x': 1}, session=s)
#             await collection.insert_one({'x': 2}, session=s)

#         # Exiting the "with s.start_transaction()" block while throwing an
#         # exception automatically aborts the transaction, exiting the block
#         # normally automatically commits it.

#         # You can run additional transactions in the same session, so long as
#         # you run them one at a time.
#         async with s.start_transaction():
#             await collection.insert_one({'x': 3}, session=s)
#             await collection.insert_many({'x': {'$gte': 2}},
#                                          {'$inc': {'x': 1}},
#                                          session=s)

# a = await coro()

async def coro(session):
    orders = session.client.db.orders
    inventory = session.client.db.inventory
    inserted_id = await orders.insert_one(
        {"sku": "abc123", "qty": 100}, session=session)
    await inventory.update_one(
        {"sku": "abc123", "qty": {"$gte": 100}},
        {"$inc": {"qty": -100}}, session=session)
    return inserted_id


async def location():
    async with await client.start_session() as session:
        inserted_id = await session.with_transaction(coro)
    # return inserted_id


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(location())


main()
