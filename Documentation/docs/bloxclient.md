#      `BloxClient`
##### *PyBlox2.RobloxWebClient.BloxClient*

## Construction
There are no required arguments to constructing a BloxClient.

You can pass `verbose=True` to print additional information on the requests.

## Methods
Methods not listed below should never be used
##### `BloxClient.connect(ROBLOSECURITY, callback)`
Where callback is your main function and ROBLOSECURITY is your bot's ROBLOSECURITY cookie. Puts the BloxClient in a connected state.

---
##### `BloxClient.get_user(username)`
Where username is the name of the user. returns a BloxUser object.

*requires BloxClient to be in a connected state*

---
##### `BloxClient.get_group(id)`
Where id is the group's id. returns a BloxGroup object.

*requires BloxClient to be in a connected state*

---
##### `BloxClient.friend_requests()`
Returns all the friend requests to the bot user.

*requires BloxClient to be in a connected state*

---
## Example

```
import PyBlox2.RobloxWebClient.BloxClient
ROBLOSECURITY = "YOUR_ROBLOSECURITY"


client = BloxClient(verbose=True)


def main():
	# do stuff
	pass


client.connect(ROBLOSECURITY, main)
```