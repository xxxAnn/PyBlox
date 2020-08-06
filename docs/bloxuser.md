# `BloxUser`
##### *PyBlox2.General.BloxUser*

## Construction
*THIS CLASS SHOULD __NEVER__ BE CONSTRUCTED*

instead obtain it via `BloxClient.get_user()`
## Methods

##### `BloxUser.accept_friend_request()`
Accept the user's friend request if there is one.

---
##### `BloxUser.decline_friend_request()`
Decline the user's friend request if there is one.

---
##### `BloxUser.request_friendship()`
Sends the user a friend request.

---
##### `BloxUser.unfriend()`
Unfriends the user.

---
##### `BloxUser.follow()`
Follows the user.

---
##### `BloxUser.unfollow()`
Unfollows the user.

---
##### `BloxUser.block()`
Blocks the user.

---
##### `BloxUser.unblock()`
Unblocks the user.

---
## Attributes

##### `BloxUser.friends`
Calls `__get_friends` internally and returns the result.

---

## Example

```
import PyBlox2.RobloxWebClient.BloxClient
ROBLOSECURITY = "YOUR_ROBLOSECURITY"


client = BloxClient(verbose=True)


def main():
	user = client.get_user("Roblox")
	print(user.friends)


client.connect(ROBLOSECURITY, main)
```

