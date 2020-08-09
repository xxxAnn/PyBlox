from secret import ROBLOSECURITY # Have your ROBLOSECURITY there
import PyBlox2
import time

# the verbose arguement could be ignored
client = PyBlox2.BloxClient(verbose=False)

# true async
@client.event
async def ready():
    await client.fetch_friend_requests()
    print(client.friend_requests)


client.run(ROBLOSECURITY)

