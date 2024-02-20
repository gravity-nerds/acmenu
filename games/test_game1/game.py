import sys

sys.path.append("../../lib")

from acproto import AcProto

protocol = AcProto("./acproto")

@protocol.onLine
def listener(*args):
    print(*args)

protocol.start()

input("TOTALLY REAL GAME\n")
