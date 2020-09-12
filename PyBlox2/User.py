import json

from .Errors import *
from .Base import BloxType
from .utils import Url

class BloxUser(BloxType):
    '''
    A handler for a roblox user
    '''
    def __init__(self, client, user_id, username):
        super().__init__(client)
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
    
    # start auto generated

    async def accept_friend_request(self):
        hook = await Url("default", "/user/accept-friend-request?requesterUserId=%id%", id=self.id).post()

    async def decline_friend_request(self):
        hook = await Url("default", "/user/decline-friend-request?requesterUserId=%id%", id=self.id).post()

    async def request_friendship(self):
        hook = await Url("default", "/user/request-friendship?recipientUserId=%id%", id=self.id).post()

    async def unfriend(self):
        hook = await Url("default", "/user/unfriend?friendUserId=%id%", id=self.id).post()

    async def follow(self):
        hook = await Url("default", "/user/follow?followedUserId=%id%", id=self.id).post()

    async def unfollow(self):
        hook = await Url("default", "/user/unfollow?followedUserId=%id%", id=self.id).post()
    
    async def block(self):
        hook = await Url("default", "/userblock/block?userId=%id%", id=self.id).post()

    async def unblock(self):
        hook = await Url("default", "/userblock/unblock?userId=%id%", id=self.id).post()

    # end auto generated

    async def fetch_friends(self):
        hook = await Url("friends", "/v1/block/users/%id%/friends", id=self.id).get()

        data = hook.json
        friend_list = []
        for user_dict in data.get("data"):
            friend_list.append(BloxUser(client=self.client, user_id=str(user_dict.get("id")), username=user_dict.get("name")))
        
        if len(friend_list) == 0:
            raise PyBloxException(
                "User has no friends"
                )

        return friend_list

    @property
    def name(self):
        return self.username
   
