from secret import ROBLOSECURITY # Have your ROBLOSECURITY there
from PyBlox2.RobloxWebClient import BloxClient


RobloxClient = BloxClient(verbose=True)


def main():
    group = RobloxClient.get_group(3891491)
    fans = group.get_role("Fan")
    print(fans.members)


RobloxClient.connect(ROBLOSECURITY, callback=main)
