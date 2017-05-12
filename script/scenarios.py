from random import choice
from time import sleep

from mbot import MetabotV2

rfcomm = "/dev/ttyACM0"
metabot = MetabotV2(rfcomm)
#TODO should try catch or maka a func
print("Connected if beep beep")
metabot.control(("play", 4))
started = True #TODO should check something before stating it's ok


scales = { #TODO could be generators (iterators ?)
    'lam':[220 + 55*i for i in range(5)] + [440 + 110*i for i in range(5)],
    'penta':[220, 440],
    'clustered':range(110, 881, 5)
}

scenarii = {
    'salute':(
        #(('freq=1.2', 0), 0),
        (('start', 0), 4),
        (('dy', 30), 5),
        (('dy', 0), 0),
        (('hello', 0), 6),
        (('dy', -30), 5),
        (('dy', 0), 0),
        (('hello', 0), 6),
        (('dy', 30), 5),
        (('dy', 0), 0),
        (('hello', 0), 6),
        (('dx', -20), 3),
        (('dx', 0), 0),
        (('stop', 0), 0)
    )
}


def check_mbot(func):
    """Decorator to check if metabot is connected"""
    def nfunc(*args):
        if started:
            return func(*args)
        else:
            print("Metabot isn't there !")
            return
    return nfunc

def act(scenario_id='salute'):
    """Play a scenario as scripted in the scenarii list"""
    for order in scenarii[scenario_id]:
        metabot.control(order[0])
        sleep(order[1])
    print('Done ' + scenario_id)
