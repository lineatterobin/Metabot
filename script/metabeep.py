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


def check_mbot(func):
    """Decorator to check if metabot is connected"""
    def nfunc(*args):
        if started:
            return func(*args)
        else:
            print("Metabot isn't there !")
            return
    return nfunc


@check_mbot
def sing(n_notes=10, scale=scales['lam'], durations=[100, 200, 400, 800]):
    for i in range(n_notes):
        dur = choice(durations)
        metabot.control(("beep", choice(scale), dur))
        sleep(dur/1000)
    print("La la laaaAAAA !!!!")
