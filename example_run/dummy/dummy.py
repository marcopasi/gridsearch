import sys, time
SLEEPTIME = 0.1  # seconds

def main(sleeptime=SLEEPTIME):
    # print(sys.argv)
    time.sleep(sleeptime)
    return sys.argv + [time.ctime()]
