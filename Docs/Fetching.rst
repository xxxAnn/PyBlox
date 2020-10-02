Fetching
=========
This sections of documentation explains the fetching feature of several items in the 
documentation.

These include:
 
:ref:`BloxClient`

:ref:`BloxUser`

:ref:`BloxMember`

:ref:`BloxRank`

.. note::
    Attributes that can be fetched will often be referred to as "``fetchable``"

Basic how-to guide
-------------------------
Fetching a fetchable is really simple:

.. code-block:: python

    client = PyBlox2.BloxClient()
    
    @client.event
    async def ready(payload):
        await client.fetch("friend_requests")

it can then be accessed through ``client.friend_requests``; However be careful as

.. code-block:: python

    client = PyBlox2.BloxClient()
    
    @client.event
    async def ready(payload):
        print(client.friend_requests)

will raise a :class:`.AttributeNotFetched` exception