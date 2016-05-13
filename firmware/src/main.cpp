#include <stdlib.h>
#include <wirish/wirish.h>
#include <terminal.h>
#include <main.h>
#include <math.h>
#include <dxl.h>
#include <function.h>
#include <commands.h>
#include <rc.h>
#include <rhock.h>
#include <servos.h>
#include "voltage.h"
#include "buzzer.h"
#include "distance.h"
#include "config.h"
#include "motion.h"
#include "leds.h"
#include "mapping.h"
#include "imu.h"
#include "bt.h"

bool isUSB = false;

#define LIT     22

bool flag = false;
bool isUSB = false;

// Time
TERMINAL_PARAMETER_FLOAT(t, "Time", 0.0);
TERMINAL_PARAMETER_FLOAT(moves_t, "Time for special moves", 0.0);

TERMINAL_COMMAND(version, "Getting firmware version")
{
    terminal_io()->print("version=");
    terminal_io()->println(METABOT_VERSION);
}

TERMINAL_COMMAND(started, "Is the robot started?")
{
    terminal_io()->print("started=");
    terminal_io()->println(started);
}

TERMINAL_COMMAND(rc, "Go to RC mode")
{
    RC.begin(921600);
    terminal_init(&RC);
    isUSB = false;
}

<<<<<<< HEAD
TERMINAL_COMMAND(learning, "Go to learning mode")
{
    terminal_io()->print("The learning mode will be enabled, ");
    terminal_io()->println("you'll need to reboot the board to return to normal operation");
    bool success;

    while (1) {
        for(int i=0; i<12; i++)
        {
            terminal_io()->print(i);
            terminal_io()->print(" ");
            terminal_io()->println(dxl_get_position(mapping[i], &success));
        }
    }
}
TERMINAL_COMMAND(learningStep, "Display motors value")
{
    bool success;
    for(int i=0; i<12; i++)
    {
        terminal_io()->print(i);
        terminal_io()->print(" ");
        terminal_io()->println(dxl_get_position(mapping[i], &success));
    }
}

void setFlag()
{
    flag = true;
}

=======
>>>>>>> b806faa67ebbe3d692cb0bd5b299f14198537a0f
// Enabling/disabling move
TERMINAL_PARAMETER_BOOL(move, "Enable/Disable move", true);


TERMINAL_COMMAND(suicide, "Lit the fuse")
{
    digitalWrite(LIT, HIGH);
}

// Setting the flag, called @50hz
bool flag = false;
void setFlag()
{
    flag = true;
}

int specialMove = NO_MOVE;
TERMINAL_COMMAND(hello, "Enable Hello movement")
{
    specialMove = HELLO_MOVE;
    moves_t = 0;
}

/**
 * Initializing
 */
void setup()
{
<<<<<<< HEAD
    RC.begin(921600);
    terminal_init(&RC);

=======
    // Initializing terminal on the RC port
    RC.begin(921600);
    terminal_init(&RC);

    // Lit pin is output low
    digitalWrite(LIT, LOW);
    pinMode(LIT, OUTPUT);

    // Initializing bluetooth module
    bt_init();

    // Initializing
>>>>>>> b806faa67ebbe3d692cb0bd5b299f14198537a0f
    motion_init();

    // Initializing voltage measurement
    voltage_init();

    // Initializing the DXL bus
    delay(500);
    dxl_init();

    // Initializing config (see config.h)
    config_init();

    // initializing distance
    distance_init();

    // Initializing the IMU
    imu_init();

    // Initializing positions to 0
    for (int i=0; i<12; i++) {
        dxl_set_position(i+1, 0.0);
    }
    for (int i=0; i<4; i++) {
        l1[i] = l2[i] = l3[i] = 0;
    }

<<<<<<< HEAD
    // Enabling 50hz ticking
    servos_init();
    servos_attach_interrupt(setFlag);
=======
    // Configuring board LED as output
    pinMode(BOARD_LED_PIN, OUTPUT);
    digitalWrite(BOARD_LED_PIN, LOW);

    // Initializing the buzzer, and playing the start-up melody
    buzzer_init();
    buzzer_play(MELODY_BOOT);

    // Enable 50hz ticking
    servos_init();
    servos_attach_interrupt(setFlag);
    
    RC.begin(921600);
>>>>>>> b806faa67ebbe3d692cb0bd5b299f14198537a0f
}

/**
 * Computing the servo values
 */
void tick()
{
    if (!move || !started) {
        t = 0.0;
        return;
    }


    if (specialMove != NO_MOVE)
    {
        if (moves_tick(moves_t, specialMove))
        {
            moves_t = 0;
            specialMove = NO_MOVE;
        }
        else
            moves_t++;
    }
    else
    {
        // Incrementing and normalizing t
        t += motion_get_f()*0.02;
        if (t > 1.0) {
            t -= 1.0;
            colorize();
        }
        if (t < 0.0) t += 1.0;

<<<<<<< HEAD
        motion_tick(t);
    }
=======
    motion_tick(t);

>>>>>>> b806faa67ebbe3d692cb0bd5b299f14198537a0f
    // Sending order to servos
    dxl_set_position(mapping[0], l1[0]);
    dxl_set_position(mapping[3], l1[1]);
    dxl_set_position(mapping[6], l1[2]);
    dxl_set_position(mapping[9], l1[3]);

    dxl_set_position(mapping[1], l2[0]);
    dxl_set_position(mapping[4], l2[1]);
    dxl_set_position(mapping[7], l2[2]);
    dxl_set_position(mapping[10], l2[3]);

    dxl_set_position(mapping[2], l3[0]);
    dxl_set_position(mapping[5], l3[1]);
    dxl_set_position(mapping[8], l3[2]);
    dxl_set_position(mapping[11], l3[3]);
}

void loop()
{
<<<<<<< HEAD
=======
    // Buzzer update
    buzzer_tick();
    // IMU ticking
    imu_tick();
    // Sampling the voltage
    voltage_tick();

>>>>>>> b806faa67ebbe3d692cb0bd5b299f14198537a0f
    // Updating the terminal
    terminal_tick();
#if defined(RHOCK)
    rhock_tick();
#endif
    if (SerialUSB.available() && !isUSB) {
        isUSB = true;
        terminal_init(&SerialUSB);
    }
<<<<<<< HEAD
=======
    if (!SerialUSB.getDTR() && isUSB) {
        isUSB = false;
        terminal_init(&RC);
    }
>>>>>>> b806faa67ebbe3d692cb0bd5b299f14198537a0f

    // Calling user motion tick
    if (flag) {
        flag = false;
        tick();
        dxl_flush();
    }
}
