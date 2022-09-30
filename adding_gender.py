import asyncio
import csv
import aiohttp
from sqlalchemy.orm import sessionmaker
from db_connection import *
from models_sql import *

# connect to db
db_engine = initiate_engine(connection_str)
connection = db_engine.connect()

# create session
Session = sessionmaker(bind=db_engine)
session = Session()
# fetch cast
cast = session.query(Netflix).with_entities(Netflix.cast).all()

session.close()

# find the unique actor names
actors = []
for row in cast:
    actors.append(row[0].split(","))
actors = [actor for sublist in actors for actor in sublist]
unique_actors = list(set(actors))

# Async API calls to retrieve the gender and write to csv.
async def main(batch):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for name in batch:
            name_for_url = "+".join(name.strip().split(" "))
            task = asyncio.ensure_future(get_actor_gender(session, name_for_url, name))
            tasks.append(task)

        gender = await asyncio.gather(*tasks)

    with open("gender.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(gender)


async def get_actor_gender(session, name_for_url, name):
    url = (
        f"https://innovaapi.aminer.cn/tools/v1/predict/gender?name="
        + name_for_url
        + "&org="
    )
    try:
        async with session.get(url) as response:
            result_data = await response.json()
            if response.status != 200:
                return {"error": f"server returned {response.status}"}
            else:
                try:
                    gender = result_data["data"]["Final"].get("gender")
                except:
                    gender = "Not Found"
                result = [name, gender]
            return result
    except asyncio.TimeoutError:
        return {"Error": f"timeout error on {url}"}


# Narrowing the parallel API calls down to 1000 per time, due to asyncio.TimeoutError.
batch_lenght = 1000
sub_lists = [
    unique_actors[i : i + batch_lenght]
    for i in range(0, len(unique_actors), batch_lenght)
]

for batch in sub_lists:
    asyncio.run(main(batch))
