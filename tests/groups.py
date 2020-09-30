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
    group = await client.get_group(3891491)
    await group.fetch("join_requests")
    print(group.join_requests)

client.run(ROBLOSECURITY)