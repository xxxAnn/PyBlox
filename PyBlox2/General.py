import json

# Local
from .Errors import *
from .Base import BloxType


def handle_response(response):
    if response.status != 200:
            raise RobloxApiError(
                response.status,
                response.text
            )
    return


def catch_error(function):

    async def wrapper(*args, **kwargs):
        response = await function(*args, **kwargs)
        if response.status != 200:
            raise RobloxApiError(
                response.status,
                response.text
            )

    return wrapper


class BloxUser(BloxType):
    '''
    A handler for a roblox user
    '''
    def __init__(self, client, user_id, username):
        super().__init__(client)
        if not isinstance(user_id, str):
            raise TypeError(
                "user_id must be a str"
                )
        self.id = str(user_id)
        self.username = username

    def __repr__(self):
        dicto = {
            "username": self.username,
            "user_id": self.id
            }

        return json.dumps(dicto)

    def __str__(self):
        return self.username
    
    @catch_error
    async def accept_friend_request(self):
        hook = await self.client.http_request(
            "POST",
            "api.roblox.com",
            "/user/accept-friend-request?requesterUserId=" + self.id
        )

        return hook

    @catch_error
    async def decline_friend_request(self):
        hook = await self.client.http_request(
            "POST",
            "api.roblox.com",
            "/user/decline-friend-request?requesterUserId=" + self.id
        )

        return hook

    @catch_error
    async def request_friendship(self):
        hook = await self.client.http_request(
            "POST",
            "api.roblox.com",
            "/user/request-friendship?recipientUserId=" + self.id
        )

        return hook

    @catch_error
    async def unfriend(self):
        hook = await self.client.http_request(
            "POST",
            "api.roblox.com",
            "/user/unfriend?friendUserId=" + self.id
        )

        return hook

    @catch_error
    async def follow(self):
        hook = await self.client.http_request(
            "POST",
            "api.roblox.com",
            "/user/follow?followedUserId=" + self.id
        )

        return hook

    @catch_error
    async def unfollow(self):
        hook = await self.client.http_request(
            "POST",
            "api.roblox.com",
            "/user/unfollow?followedUserId=" + self.id
        )

        return hook
    
    @catch_error
    async def block(self):
        hook = await self.client.http_request(
            "POST",
            "api.roblox.com",
            "/userblock/block?userId=" + self.id
        )
    
        return hook

    @catch_error
    async def unblock(self):
        hook = await self.client.http_request(
            "POST",
            "api.roblox.com",
            "/userblock/unblock?userId=" + self.id
        )

        return hook
    
    async def fetch_friends(self):
        hook = await self.client.http_request(
            "GET",
            "friends.roblox.com",
            "/v1/users/" + self.id + "/friends"
            )
        try:
            handle_response(hook)
        except RobloxApiError:
            return

        data = json.loads(hook.text)
        friend_list = []
        for user_dict in data.get("data"):
            friend_list.append(BloxUser(client=self.client, user_id=str(user_dict.get("id")), username=user_dict.get("name")))
        
        if len(friend_list) == 0:
            raise PyBloxException(
                "User has no friends"
                )

        self._friends = friend_list
        return friend_list
    
    @property
    def friends(self):
        if hasattr(self, '_friends'):
            return self._friends
        else:
            raise AttributeNotFetched(
                    "friends"
                )
