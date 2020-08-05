import json
import RobloxApi.RobloxApiError as ErrorModule



class BloxUser:
    '''
    This shouldn't ever be manually constructed, rather BloxClient.get_user should be used.
    Implements all the methods the Roblox API allows us to
    '''
    def __init__(self, client, user_id, username):
        self.id = str(user_id)
        self.client = client
        self.username = username
    
    def __str__(self):
        return self.username

    def accept_friend_request(self):
        hook = self.client.webClient.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/accept-friend-request?requesterUserId=" + self.id
        )

    def decline_friend_request(self):
        hook = self.client.webClient.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/decline-friend-request?requesterUserId=" + self.id
        )

    def request_friendship(self):
        hook = self.client.webClient.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/request-friendship?recipientUserId=" + self.id
        )

    def unfriend(self):
        hook = self.client.webClient.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/unfriend?friendUserId=" + self.id
        )

    def follow(self):
        hook = self.client.webClient.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/follow?followedUserId=" + self.id
        )

    def unfollow(self):
        hook = self.client.webClient.httpRequest(
            "POST",
            "api.roblox.com",
            "/user/unfollow?followedUserId=" + self.id
        )

    def block(self):
        hook = self.client.webClient.httpRequest(
            "POST",
            "api.roblox.com",
            "/userblock/block?userId=" + self.id
        )

    def unblock(self):
        hook = self.client.webClient.httpRequest(
            "POST",
            "api.roblox.com",
            "/userblock/unblock?userId=" + self.id
        )

    
