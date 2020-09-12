# PyBlox2

High level library for making Roblox bots in Python
### Examples
#### A Basic Example
```python
import PyBlox2
import time

client = PyBlox2.BloxClient()

@client.event
async def ready(ctx):
    await client.fetch("friend_requests")
    player = client.friend_requests[0]
    await player.fetch("friends")
    
    (player.friends[0])

@client.event
async def request(ctx):
    print("Received status code ", ctx[0].status)

client.run(ROBLOSECURITY) # ROBLOSECURITY COOKIE
```
#### Changing someone's role
```python
import PyBlox2
import time

client = PyBlox2.BloxClient()

@client.event
async def ready(ctx):
    group = await client.get_group(5029105)
    member = await group.get_member("fego2015")
    role = await group.get_role("Moderators")
    await member.set_role(role)

@client.event
async def request(ctx):
    print("Received status code ", ctx[0].status)

client.run(ROBLOSECURITY) # ROBLOSECURITY COOKIE
```