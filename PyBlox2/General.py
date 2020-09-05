import json

# Local
from .Errors import *
from .Base import BloxType
from .utils.Endpoints import *

def handle_response(response):
    if response.status != 200:
            raise RobloxApiError(
                response.status,
                response.text
            )
    return

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
        self.can_fetch("friends")

    def __repr__(self):
        _dict = {
            "username": self.username,
            "user_id": self.id
            }

        return json.dumps(_dict)

    def __str__(self):
        return self.username
    
    @catch_error
    async def accept_friend_request(self):
        hook = await self.client.http_request(
            "POST",
            DEFAULT_ENDPOINT,
            "/user/accept-friend-request?requesterUserId=" + self.id
        )

        return hook

    @catch_error
    async def decline_friend_request(self):
        hook = await self.client.http_request(
            "POST",
            DEFAULT_ENDPOINT,
            "/user/decline-friend-request?requesterUserId=" + self.id
        )

        return hook

    @catch_error
    async def request_friendship(self):
        hook = await self.client.http_request(
            "POST",
            DEFAULT_ENDPOINT,
            "/user/request-friendship?recipientUserId=" + self.id
        )

        return hook

    @catch_error
    async def unfriend(self):
        hook = await self.client.http_request(
            "POST",
            DEFAULT_ENDPOINT,
            "/user/unfriend?friendUserId=" + self.id
        )

        return hook

    @catch_error
    async def follow(self):
        hook = await self.client.http_request(
            "POST",
            DEFAULT_ENDPOINT,
            "/user/follow?followedUserId=" + self.id
        )

        return hook

    @catch_error
    async def unfollow(self):
        hook = await self.client.http_request(
            "POST",
            DEFAULT_ENDPOINT,
            "/user/unfollow?followedUserId=" + self.id
        )

        return hook
    
    @catch_error
    async def block(self):
        hook = await self.client.http_request(
            "POST",
            DEFAULT_ENDPOINT,
            "/userblock/block?userId=" + self.id
        )
    
        return hook

    @catch_error
    async def unblock(self):
        hook = await self.client.http_request(
            "POST",
            DEFAULT_ENDPOINT,
            "/userblock/unblock?userId=" + self.id
        )

        return hook
    
    async def fetch_friends(self):
        hook = await self.client.http_request(
            "GET",
            FRIENDS_ENDPOINT,
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

        return friend_list
   
