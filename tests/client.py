import logging
import sys
import os
sys.path.append(os.getcwd())

import PyBlox2

from secret import ROBLOSECURITY

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s.%(funcName)s: %(message)s'
    )
client = PyBlox2.BloxClient(prefix="!")

@client.event
async def ready(payload):
    assert payload == "I'm ready"
    friend_requests = await client.fetch("friend_requests")
    await friend_requests[1].accept_friend_request() # Accept a friend request

client.run(ROBLOSECURITY)