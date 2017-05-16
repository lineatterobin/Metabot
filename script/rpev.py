import tty
import sys
import termios
import serial
import threading
import random

random.seed()

term = None


def menu_factory(m):
    def func(state):
        state['menu'] = m
        print(m['name'])
    return func


def rd():
    while True:
        print(term.read().decode('utf-8'), end='')
read_thread = threading.Thread(target=rd)


def command(com):
    term.write((com+'\r').encode('utf-8'))


def beep_command(freq):
    command('beep ' + str(freq) + ' 10000')


def co(port="/dev/ttyACM0"):
    global term
    term = serial.Serial(port=port, baudrate=115200)
    read_thread.start()
    command('version')


def start_stop(state):
    if state['started']:
        command('stop')
        state['started'] = False
    else:
        command('start')
        state['started'] = True


def beep_factory(midi=None, freq=None):
    if not freq:
        if midi:
            freq = 2**((midi - 69)/12) * 440
        else:
            freq = 0

    def func(unused):
        del unused
        beep_command(freq)
    return func


def beep_rand_factory(min_freq):
    def func(unused):
        del unused
        beep_command(min_freq + random.random()*100)
    return func

commands = {
    'name': 'commands',
    '\r': start_stop
}

beep_keys = ['a', 'é', 'z', '"', 'e', 'r', '(', 't', '-', 'y', 'è', 'u',
             'w', 's', 'x', 'd', 'c', 'v', 'g', 'b', 'h', 'n', 'j', ',',
             'A', '2', 'Z', '3', 'E', 'R', '5', 'T', '6', 'Y', '7', 'U',
             'W', 'S', 'X', 'D', 'C', 'V', 'G', 'B', 'H', 'N', 'J', '?']
beep_rand = ['_', 'ç', 'à', ')', '=', 'i', 'o', 'p', '^', '$',
             'k', 'l', 'm', 'ù', '*', ';', ':', '!']

beeps = {
    'name': 'beeps',
    '>': menu_factory(commands),
    ' ': beep_factory()
}

beeps.update({beep_keys[i]: beep_factory(i+48) for i in range(len(beep_keys))})
beeps.update({beep_rand[i]: beep_rand_factory(50 + 100*i) for i in range(len(beep_rand))})

commands.update({'B': menu_factory(beeps)})


def keys():
    state = {
        'menu': commands,
        'started': False
    }

    orig_settings = termios.tcgetattr(sys.stdin)

    tty.setraw(sys.stdin)
    x = 0
    try:
        while x != chr(27):  # ESC
            x = sys.stdin.read(1)[0]
            if x in state['menu']:
                state['menu'][x](state)
            else:
                print('Nothing for ', x)
    except Exception:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
