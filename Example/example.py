from secret import ROBLOSECURITY # Have your ROBLOSECURITY there
import PyBlox2
import time


client = PyBlox2.BloxClient(verbose=False)


def main():
    group = client.get_group(5029105)
    try:
        print(group.join_requests)
    except PyBlox2.PyBloxException:
        print(group)


client.connect(ROBLOSECURITY, callback=main)

