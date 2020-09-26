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

from .User import BloxUser
from .Ranks import BloxRank
from .utils import Url
from .Errors import *

class BloxMember(BloxUser):

    def __init__(self, client, user_id: str, username: str, group):
        super().__init__(client=client, user_id=user_id, username=username)
        self.group = group
        self.__access = Url("groups", "/v1/groups/%group_id%/users/%user_id%", group_id=self.group.id, user_id=self.id) 

    async def set_role(self, role: BloxRank):
        '''
        Changes the user's role in the group
        '''
        payload = "{\"roleId\":" + str(role.id) + "}"
        try:
            await self.__access.patch(payload)
        except UnknownClientError as e:
            if e.data.json['errors'][0]['code'] == 3:
                raise NilInstance
    
    async def kick(self):
        '''
        kicks the user from the group
        '''
        await self.__access.delete()