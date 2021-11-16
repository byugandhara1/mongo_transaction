import motor.motor_asyncio
import asyncio

from pymongo import WriteConcern

from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

# For a replica set, include the replica set name and a seedlist of the members in the URI string; e.g.
uriString = 'mongodb://0.0.0.0:27017,0.0.0.0:27018/?replicaSet=myRepl'
# For a sharded cluster, connect to the mongos instances; e.g.
# uriString = 'mongodb://mongos0.example.com:27017,mongos1.example.com:27017/'

client = motor.motor_asyncio.AsyncIOMotorClient(uriString)
wc_majority = WriteConcern("majority", wtimeout=1000)


# Step 1: Define the callback that specifies the sequence of operations to perform inside the transactions.

async def callback(my_session):
    collection_one = my_session.client.mydb1.foo
    collection_two = my_session.client.mydb2.bar

    # Important:: You must pass the session to the operations.
    await collection_one.insert_one({'abc': 1}, session=my_session)
    await collection_two.insert_one({'xyz': 999}, session=my_session)


async def execute():

    # Prereq: Create collections.
    await client.get_database(
        "mydb1", write_concern=wc_majority).foo.insert_one({'abc': 0})
    await client.get_database(
        "mydb2", write_concern=wc_majority).bar.insert_one({'xyz': 0})

    # Step 2: Start a client session.
    async with await client.start_session() as session:
        # Step 3: Use with_transaction to start a transaction, execute the callback, and commit (or abort on error).
        await session.with_transaction(
            callback, read_concern=ReadConcern('local'),
            write_concern=wc_majority,
            read_preference=ReadPreference.PRIMARY)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute())


main()
