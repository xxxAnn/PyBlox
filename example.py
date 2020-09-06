from secret import ROBLOSECURITY
import PyBlox2

client = PyBlox2.BloxClient(prefix="!")

@client.event
async def ready(payload):
    await client.fetch("friend_requests")
    player = client.friend_requests[0]
    await player.fetch("friends")
    print(player.friends[0])

@client.command
async def ping(ctx, text):
    print('pong ', text)

@client.event
async def error(ctx, error):
    print(ctx.user, " caused an error <unhappy face>")

client.run(ROBLOSECURITY, group_id=3891491)

