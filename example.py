from secret import ROBLOSECURITY # Have your ROBLOSECURITY there
import PyBlox2
import time

# the verbose arguement could be ignored
client = PyBlox2.BloxClient()

@client.event
async def ready(ctx):
    await client.fetch("friend_requests")
    player = client.friend_requests[0]
    await player.fetch("friends")
    print(player.friends[0])

@client.event
async def request(ctx):
    pass
    print("Received status code ", ctx[0].status)

client.run(ROBLOSECURITY) # ROBLOSECURITY COOKIE

