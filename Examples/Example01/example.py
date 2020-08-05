from secret import ROBLOSECURITY # Have your ROBLOSECURITY there
from PyBlox2.RobloxWebClient import BloxClient


RobloxClient = BloxClient()


def main():
    member = RobloxClient.get_group(3891491).get_member("Kate_tsu")
    print(member)


RobloxClient.connect(ROBLOSECURITY, callback=main)
