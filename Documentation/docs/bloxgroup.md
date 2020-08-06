# `BloxGroup`
##### *PyBlox2.Groups.BloxGroup*

## Construction
*THIS CLASS SHOULD __NEVER__ BE CONSTRUCTED*

instead obtain it via `BloxClient.get_group()`
## Methods

##### `BloxGroup.get_role(role_set_name)`
Returns a `BloxRank` object with the selected role_set_name.

---
##### `BloxGroup.get_role(username)`
Returns a `BloxMember` object with the selected username.

---
##### `BloxGroup.members()`
*This is will be deprecated in the next update*

---
Returns a list of `BloxMember` objects, all the members of the Group.

---
## Attributes

##### `BloxUser.join_requests`
*This currently doesn't work*

Calls `__join_requests` internally and returns the result.

---
##### `BloxUser.settings`
Calls `__get_setings` internally and returns a BloxSettings object with the guild's settings.

---