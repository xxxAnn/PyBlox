import logging

import PyBlox2

from secret import ROBLOSECURITY

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s.%(funcName)s: %(message)s'
    )
client = PyBlox2.BloxClient(prefix="!")


@client.event
async def ready(payload):
    # Executed as a callback of coro client.__http.connect 
    #
    # Will receive "I'm ready" as payload, otherwise something
    # went wrong with the emitter
    #
    # Client.user is the BloxUser object of the client
    # that object does not get cached so it should
    # always be accessed with client.user
    # instead of trying to do something similar to
    # client.get_user(client.user.name) or the likes of it
    assert payload == "I'm ready"
    print("xx---xx")
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("xx---xx")
    # Checking the group wall starts here

@client.command
async def ping(ctx, text):
    # Commands can have any kind and amount of arguments
    # however the first argument is always "context" 
    # 
    # If the amount of arguments from the command on the group wall
    # Doesn't match the amount of arguments in the command here
    # then PyBlox2.BadArgument will be raised
    print('pong ', text)

@client.event
async def error(ctx, error):
    print(ctx.user, " caused an error <unhappy face>")

@client.event
async def start_listening(guild):
    # Executed as a callback of coro client.__commander.start_loop 
    #                                                               
    # Returns a Guild object, that might be obtained from the cache 
    #                                                               
    #            Will only receive the guild parameter              
    await guild.fetch("name")
    # When printing guild, if name is fetched it will print the name
    # Otherwise it will error
    print("Listening to guild", guild)

# If a group_id is provided here then it will be
# listened to for any commands or message
# 
# On the other hand if the argument is ignored then
# the code will shutdown after executing the ready event
#
# client.run IS a blocking call meaning that any code
# after it will not be executed until its finished
client.run(ROBLOSECURITY, group_id=3891491)

