import logging

import PyBlox2

from secret import ROBLOSECURITY

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s.%(funcName)s: %(message)s'
    )
client = PyBlox2.BloxClient(prefix="!")


@client.event
async def ready(payload):
    assert payload == "I'm ready"
    print("xx---xx")
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("xx---xx")
    user = await client.get_user(user_id=182262920)
    assert user.name == "fego2015"

@client.command
async def ping(ctx, text):
    print(text)

@client.event
async def error(ctx, error):
    print("An error has occured")

@client.event
async def start_listening(guild):
    await guild.fetch("name")
    print("Listening to guild", guild)

client.run(ROBLOSECURITY) # , group_id=3891491