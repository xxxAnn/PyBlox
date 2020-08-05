from secret import ROBLOSECURITY
from RobloxWebClient import BloxClient


RobloxClient = BloxClient()


def main():
    members = RobloxClient.get_group(5029105).members()
    for member in members:
        print(str(member) + '\n')


RobloxClient.connect(ROBLOSECURITY, callback=main)
