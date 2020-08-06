import json

# Local
from .RobloxApiError import *


def handle_response(response):
    if response.status != 200:
            raise RobloxApiError(
                response.status,
                response.read().decode("utf-8")
            )
    return


class BloxUser:
    '''
    This shouldn't ever be manually constructed, rather BloxClient.get_user should be used.
    Implements all the methods the Roblox API allows us to
    '''
    def __init__(self, client, user_id, username):
        self.id = str(user_id)
        self.client = client
        self.username = username

    def __repr__(self):
        dicto = {
            "username": self.username,
            "user_id": self.id
            }

        return json.dumps(dicto)

    def __getattr__(self, item):
        if item == "friends":
            friends = self.__get_friends()
            return friends

    def __str__(self):
        return self.username

    def accept_friend_request(self):
        hook = self.client.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/accept-friend-request?requesterUserId=" + self.id
        )

    def decline_friend_request(self):
        hook = self.client.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/decline-friend-request?requesterUserId=" + self.id
        )

    def request_friendship(self):
        hook = self.client.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/request-friendship?recipientUserId=" + self.id
        )

    def unfriend(self):
        hook = self.client.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/unfriend?friendUserId=" + self.id
        )

    def follow(self):
        hook = self.client.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/follow?followedUserId=" + self.id
        )

    def unfollow(self):
        hook = self.client.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/unfollow?followedUserId=" + self.id
        )

    def block(self):
        hook = self.client.httpRequest(
            "POST",
            "api.roblox.com",
            "/userblock/block?userId=" + self.id
        )

    def unblock(self):
        hook = self.client.httpRequest(
            "POST",
            "api.roblox.com",
            "/userblock/unblock?userId=" + self.id
        )
    
    def __get_friends(self):
        '''
        Should only be used locally
        '''
        if use_cache:
            return self.cached_friends
        hook = self.cliewnt.httpRequest(
            "GET",
            "friends.roblox.com",
            "/v1/users/" + self.id + "/friends"
            )
        try:
            handle_response(hook)
        except RobloxApiError:
            return

        data = json.loads(hook.read().decode("utf-8"))
        friend_list = []
        for user_dict in data.get("data"):
            friend_list.append(BloxUser(client=self.client, user_id=str(user_dict.get("id")), username=user_dict.get("name")))
        self.cached_friends = friend_list
        
        return friend_list