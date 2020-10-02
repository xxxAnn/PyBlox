import json

from .Errors import *
from .Base import BloxType
from .utils import Url

class BloxUser(BloxType):
    """
    A handler for a roblox user

    .. note::
        This class shouldn't manually be created

    Attributes
    ----------
    id: :class:`str`
        The userId of the user
    username: :class:`str`
        The username of the user
    friends: list[:class:`.BloxUser`]
        |fch|

        List of this user's friends
    """
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
        """|coro|

        Accepts a friend request from a user
        
        Raises
        -------
        :exc:`.NilInstance`
            Attempted manipulation on non existing instance
        :exc:`.UserBlocked`
            Attempted to interact with a blocked user
        """
        try:
            hook = await Url("friends", "/v1/users/%id%/accept-friend-request", id=self.id).post()
        except Forbidden:
            raise UserBlocked
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def decline_friend_request(self):
        """|coro|

        Declines a friend request from a user
        
        Raises
        -------
        :exc:`.NilInstance`
            Attempted manipulation on non existing instance

        """
        try:
            hook = await Url("friends", "/v1/users/%id%/decline-friend-request", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def request_friendship(self):
        """|coro|

        Sends a friend request to the user

        .. warning::
            Will be deprecated in 1.1 in favor of add_friend

        Raises
        -------
        :exc:`.NilInstance`
            Attempted manipulation on non existing instance
        """
        try: 
            hook = await Url("default", "/user/request-friendship?recipientUserId=%id%", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def unfriend(self):
        """|coro|

        Unfriends the user
        
        Raises
        -------
        :exc:`.NilInstance`
            Attempted manipulation on non existing instance
        """
        try:
            hook = await Url("friends", "/v1/users/%id%/unfriend", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def follow(self):
        """|coro|

        Follows the user
        
        Raises
        -------
        :exc:`.NilInstance`
            Attempted manipulation on non existing instance
        """
        try:
            hook = await Url("friends", "/v1/users/%id%/follow", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance
        except Forbidden:
            raise UserBlocked

    async def unfollow(self):
        """|coro|

        Unfollows the user
        
        Raises
        -------
        :exc:`.NilInstance`
            Attempted manipulation on non existing instance
        """
        try:
            hook = await Url("friends", "/v1/users/%id%/unfollow", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance
    
    async def block(self):
        """|coro|

        Blocks the user
        
        Raises
        -------
        :exc:`.NilInstance`
            Attempted manipulation on non existing instance
        """
        try:
            hook = await Url("default", "/userblock/block?userId=%id%", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def unblock(self):
        """|coro|

        Unblocks the user
        
        Raises
        -------
        :exc:`.NilInstance`
            Attempted manipulation on non existing instance
        """
        try:
            hook = await Url("default", "/userblock/unblock?userId=%id%", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

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
   
