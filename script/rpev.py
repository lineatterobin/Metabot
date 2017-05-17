import tty
import sys
import termios
import serial
import threading
import random
import inputs

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


# ---------------- MAIN FUNCS ----------------

def menu_factory(m):
    def func(state):
        state['menu'] = m
        print(m['name'])
    return func


def start_stop(state):
    if state['started']:
        command('stop')
        state['started'] = False
    else:
        command('start')
        state['started'] = True


# ---------------- GAMEPAD FUNCS ----------------

gamepad_state = {
    'l_stick': {'x': 0, 'y': 0, 'btn': 0},  # x => right ; y => down
    'r_stick': {'x': 0, 'y': 0, 'btn': 0},  # +/- 2^15 (32768) ~10% giggle
    'pad': {'up': 0, 'down': 0, 'left': 0, 'right': 0},
    'triggers': {'left': 0, 'right': 0},  # 0-255
    'shoulders': {'left': 0, 'right': 0},
    'start': 0,
    'select': 0,
    'mode': 0,
    'a': 0,
    'b': 0,
    'x': 0,
    'y': 0
}
gamepad_state_lock = threading.Lock()

event_interpretation = {
    'ABS_X': ['l_stick', 'x'],
    'ABS_Y': ['l_stick', 'y'],
    'BTN_THUMBL': ['l_stick', 'btn'],
    'ABS_RX': ['r_stick', 'x'],
    'ABS_RY': ['r_stick', 'y'],
    'BTN_THUMBR': ['r_stick', 'btn'],
    'ABS_HAT0X': ['pad', 'left', 'right'],
    'ABS_HAT0Y': ['pad', 'up', 'down'],
    'ABS_Z': ['triggers', 'left'],
    'ABS_RZ': ['triggers', 'right'],
    'BTN_TL': ['shoulders', 'left'],
    'BTN_TR': ['shoulders', 'right'],
    'BTN_START': ['start'],
    'BTN_SELECT': ['select'],
    'BTN_MODE': ['mode'],
    'BTN_SOUTH': ['a'],
    'BTN_EAST': ['b'],
    'BTN_NORTH': ['x'],
    'BTN_WEST': ['y']
}


def gamepad_event_loop():
    while True:
        events = inputs.get_gamepad()
        for event in events:
            if event.ev_type != "Sync":
                if event.code in event_interpretation:
                    path = event_interpretation[event.code]
                    gamepad_state_lock.acquire()
                    if len(path) == 1:
                        gamepad_state[path[0]] = event.state
                    elif len(path) == 2:
                        gamepad_state[path[0]][path[1]] = event.state
                    else:  # Weird HAT0X/Y for pad
                        if event.state > 0:
                            gamepad_state[path[0]][path[2]] = event.state
                        elif event.state < 0:
                            gamepad_state[path[0]][path[1]] = -event.state
                        else:
                            gamepad_state[path[0]][path[2]] = event.state
                            gamepad_state[path[0]][path[1]] = -event.state
                    gamepad_state_lock.release()
                else:
                    print("Unknown event: ", event.code, event.state)
        print(gamepad_state)

gamepad_thread = threading.Thread(target=gamepad_event_loop)
gamepad_thread.start()


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

# ================ GAMEPAD MAPPINGS ================

mappings = {
    'name': 'mappings',
    '>': menu_factory(commands)
}

# Access from main menu
commands['M'] = menu_factory(mappings)

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

# Access from main menu
commands['B'] = menu_factory(beeps)

# ================ LEDS ================

# Auto-populate main menu:
# 1: Blue
# 2: Green
# 3: Cyan
# 4: Red
# 5: Magenta
# 6: Yellow(ish)
# 7: White
# 0: Off
# .: Decustom
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
