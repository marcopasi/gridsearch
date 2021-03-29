import sys, time

def main(sleeptime=0):
    # print(sys.argv)
    time.sleep(sleeptime)
    return sys.argv + [time.ctime()]
