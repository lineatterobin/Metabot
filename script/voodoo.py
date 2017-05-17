#!/usr/bin/python3
from serial import Serial
import time

# Update frequency (Hz)
frequency = 15

# Metabot input
metabotInput = Serial('/dev/ttyACM0', timeout=0.1)

# Metabot output
metabotOutput = Serial('/dev/pink')

# Write timeout
metabotInput.write_timeout = 0.5
metabotOutput.write_timeout = 1

# Try/except because of write timeouts
try:
    metabotInput.write(b"stop\rlearning\r")
except:
    pass
try:
    metabotOutput.write(b"specialmove\rstart\r")
except:
    pass

print('Waiting')
time.sleep(5)

# Position of motors from the input robot
angles = [0 for x in range(12)]

# Buffer
data = u""

# Timestamp for last update
last = 0

while True:
    # Reading data
    data += metabotInput.read(128).decode('ascii')
    # Splitting it using \n
    parts = data.split("\n")
    while len(parts) > 1:
        info = parts.pop(0).split(' ')
        if len(info) == 2:
            # Updating the position of a motro
            try:
                idx = int(info[0])
                angles[idx] = 0.5*angles[idx] + 0.5*float(info[1])
            except:
                pass
    # print(angles)

    if time.time()-last > 1.0/frequency:
        last = time.time()
        # Sending the position of the motors using motor1 and motor2
        try:
            values=angles[0:6]
            values+=[sum(values)]
            metabotOutput.write(("motor1 "+' '.join('%.1f' % x for x in values)+"\r").encode('ascii'))
            metabotOutput.reset_input_buffer()
            values=angles[6:12]
            values+=[sum(values)]
            metabotOutput.write(("motor2 "+' '.join('%.1f' % x for x in values)+"\r").encode('ascii'))
            metabotOutput.reset_input_buffer()
        except:
            print('Write error')
            pass
    data = "\n".join(parts)

