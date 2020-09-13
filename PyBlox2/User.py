"""
The MIT License (MIT)

Copyright (c) Kyando 2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
        hook = await Url("friends", "/v1/users/%id%/friends", id=self.id).get()

        data = hook.json
        friend_list = []
        for user_dict in data.get("data"):
            friend_list.append(BloxUser(client=self.client, user_id=str(user_dict.get("id")), username=user_dict.get("name")))
        
        if len(friend_list) == 0:
            raise PyBloxException(
                "User has no friends"
                )

        return friend_list

    # Aliases

    @property
    def name(self):
        return self.username

    async def add_friend(self, *args, **kwargs):
        await self.request_friendship()
   
