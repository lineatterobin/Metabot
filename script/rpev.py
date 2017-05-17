import tty
import sys
import termios
import serial
import threading
import random

random.seed()

# To forward tty output with a thread
term = None
term_lock = threading.Lock()


def read_int_tty_loop():
    while True:
        term_lock.acquire()
        print(term.read().decode('utf-8'), end='')
        term_lock.release()
read_thread = threading.Thread(target=read_int_tty_loop)


# Generic to write a command to the tty
def command(com):
    term_lock.acquire()
    term.write((com+'\r').encode('utf-8'))
    term_lock.release()


# Establishing the connection (plus read thread & check connection with version)
def co(port="/dev/ttyACM0"):
    global term
    term = serial.Serial(port=port, baudrate=115200)
    read_thread.start()
    command('version')


# Factory for generic function to change menu
def menu_factory(m):
    def func(state):
        state['menu'] = m
        print(m['name'])
    return func


# Alternatively starts and stops, not checking it worked
def start_stop(state):
    if state['started']:
        command('stop')
        state['started'] = False
    else:
        command('start')
        state['started'] = True


# ---------------- BEEPS FUNCS ----------------

def beep_command(freq):
    command('beep ' + str(freq) + ' 10000')


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


# ---------------- LEDS FUNCS ----------------

def led_factory(color):
    def func(unused):
        del unused
        if color is None:
            command('led')
        else:
            command('led ' + str(color))
    return func

# ---------------- MENUS ----------------

# ================ MAIN ================

commands = {
    'name': 'commands',
    '\r': start_stop
}

# ================ BEEPS ================

# Piano keyboard
beep_keys = ['a', 'é', 'z', '"', 'e', 'r', '(', 't', '-', 'y', 'è', 'u',
             'w', 's', 'x', 'd', 'c', 'v', 'g', 'b', 'h', 'n', 'j', ',',
             'A', '2', 'Z', '3', 'E', 'R', '5', 'T', '6', 'Y', '7', 'U',
             'W', 'S', 'X', 'D', 'C', 'V', 'G', 'B', 'H', 'N', 'J', '?']

# Remaining keys to random beep
beep_rand = ['_', 'ç', 'à', ')', '=', 'i', 'o', 'p', '^', '$',
             'k', 'l', 'm', 'ù', '*', ';', ':', '!']

beeps = {
    'name': 'beeps',
    '>': menu_factory(commands),
    ' ': beep_factory()
}

# Populate with above key maps
beeps.update({beep_keys[i]: beep_factory(i+48) for i in range(len(beep_keys))})
beeps.update({beep_rand[i]: beep_rand_factory(50 + 100*i) for i in range(len(beep_rand))})

commands.update({'B': menu_factory(beeps)})

# ================ LEDS ================

# Auto-populate :
# 1 : Blue
# 2 : Green
# 3 : Cyan
# 4 : Red
# 5 : Magenta
# 6 : Yellow(ish)
# 7 : White
# 0 : Off
# . : Decustom
commands.update({str(i): led_factory(i) for i in range(8)})
commands['.'] = led_factory(None)


# |-|-|-|-|-|-|-|-| Main function |-|-|-|-|-|-|-|-|

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
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
