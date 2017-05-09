#include <stdio.h>
#include <math.h>
#ifdef HAS_TERMINAL
#include <terminal.h>
#else
#define TERMINAL_PARAMETER_BOOL(name, desc, def) \
    bool name = def;
#define TERMINAL_PARAMETER_FLOAT(name, desc, def) \
    float name = def;
#define TERMINAL_PARAMETER_DOUBLE(name, desc, def) \
    double name = def;
#define TERMINAL_PARAMETER_INT(name, desc, def) \
    int name = def;
#endif
#ifdef __EMSCRIPTEN__
#include <emscripten/bind.h>
#endif
#ifdef RHOCK
#include <rhock/event.h>
#include <rhock/stream.h>
#endif

#include "function.h"
#include "kinematic.h"
#include "music.h"

TERMINAL_PARAMETER_FLOAT(freqLeg1, "Leg 1's freq", 0.0);
TERMINAL_PARAMETER_FLOAT(freqLeg2, "Leg 2's freq", 0.0);
TERMINAL_PARAMETER_FLOAT(freqLeg3, "Leg 3's freq", 0.0);
TERMINAL_PARAMETER_FLOAT(freqLeg4, "Leg 4's freq", 0.0);

#define MODE_PERC       0
#define MODE_GLIDE      1

TERMINAL_PARAMETER_INT(modeLeg1, "Mode (0:Perc, 1:GLIDE, 2:SCRATCH)", MODE_PERC);
TERMINAL_PARAMETER_INT(modeLeg2, "Mode (0:Perc, 1:GLIDE, 2:SCRATCH)", MODE_PERC);
TERMINAL_PARAMETER_INT(modeLeg3, "Mode (0:Perc, 1:GLIDE, 2:SCRATCH)", MODE_PERC);
TERMINAL_PARAMETER_INT(modeLeg4, "Mode (0:Perc, 1:GLIDE, 2:SCRATCH)", MODE_PERC);

TERMINAL_PARAMETER_FLOAT(phaseLeg1, "Leg 1's phase", 0.0);
TERMINAL_PARAMETER_FLOAT(phaseLeg2, "Leg 2's phase", 0.0);
TERMINAL_PARAMETER_FLOAT(phaseLeg3, "Leg 3's phase", 0.0);
TERMINAL_PARAMETER_FLOAT(phaseLeg4, "Leg 4's phase", 0.0);

TERMINAL_COMMAND(freqLegs, "Set all freqLeg") {
    if (argc > 0) {
        freqLeg1 = atof(argv[0]);
        freqLeg2 = atof(argv[0]);
        freqLeg3 = atof(argv[0]);
        freqLeg4 = atof(argv[0]);
    }
    else {
        freqLeg1 = 0;
        freqLeg2 = 0;
        freqLeg3 = 0;
        freqLeg4 = 0;
    }
}

float Lg[4] = {0.0,0.0,0.0,0.0};

TERMINAL_COMMAND(Leg1, "Execute a single movement with the leg 1.") {
    Lg[0] = 0.0;
}
TERMINAL_COMMAND(Leg2, "Execute a single movement with the leg 2.") {
    Lg[1] = 0.0;
}
TERMINAL_COMMAND(Leg3, "Execute a single movement with the leg 3.") {
    Lg[2] = 0.0;
}
TERMINAL_COMMAND(Leg4, "Execute a single movement with the leg 4.") {
    Lg[3] = 0.0;
}

Function perc;
Function glide;

void setup_music_functions()
{
    perc.clear();
    glide.clear();

    perc.addPoint(0.0, 0.0);
    perc.addPoint(0.1, -30.0);
    perc.addPoint(0.3, -30.0);
    perc.addPoint(0.35, 0.0);
    perc.addPoint(1.0, 0.0);

    glide.addPoint(0.0, 0.0);
    glide.addPoint(0.2, -25.0);
    glide.addPoint(0.5, -50.0);
    glide.addPoint(0.8, -25.0);
    glide.addPoint(1.0, 0.0);

}

#define TMAX 10000
float tps = 0;

float motion_music(int motor, int leg, float freq) {
    setup_music_functions();
    float freqLeg;
    float phase;
    int mode;

    if (motor==3) {
        tps += freq;
        if (tps > TMAX) {
            tps -= TMAX;
        }
        if (tps < 0.0) tps+=freq;
    }

    switch(leg) {
    case 0:
        phase = phaseLeg1;
        freqLeg = freqLeg1;
        mode = modeLeg1;
        break;
    case 1:
        phase = phaseLeg2;
        freqLeg = freqLeg2;
        mode = modeLeg2;
        break;
    case 2:
        phase = phaseLeg3;
        freqLeg = freqLeg3;
        mode = modeLeg3;
        break;
    case 3:
        phase = phaseLeg4;
        freqLeg = freqLeg4;
        mode = modeLeg4;
        break;
    default:
        freqLeg = 0;
        mode = MODE_PERC;
        break;
    }

    switch(mode) { //Add more modes in this switch
    case MODE_PERC:
        if (motor==2)
            return perc.getMod((freqLeg*tps)/(TMAX*1.0) + phase);
        else
            return 0.0;
        break;
    case MODE_GLIDE:
        if (motor==3 || motor==2)
            return glide.getMod((freqLeg*tps)/(TMAX*1.0) + phase);
        else
            return 0.0;
        break;
    default:
        return 0.0;
        break;
    }
}

float motion_impro(int motor, int leg) {

    if (Lg[leg] <= 1.0) {
        setup_music_functions();

        int mode;

        switch(leg) {
        case 0:
            mode = modeLeg1;
            break;
        case 1:
            mode = modeLeg2;
            break;
        case 2:
            mode = modeLeg3;
            break;
        case 3:
            mode = modeLeg4;
            break;
        default:
            mode = MODE_PERC;
            break;
        }

        float res = 0;

        switch(mode) { //Add more modes in this switch
        case MODE_PERC:
            if (motor==2)
                return perc.getMod(Lg[leg]);
            else if (motor==3) {
                Lg[leg] = Lg[leg] + 0.1;
                return 0.0;
            }
            else
                return 0.0;
            break;
        case MODE_GLIDE:
            if (motor==2)
                return glide.getMod(Lg[leg]);
            else if (motor==3) {
                res = glide.getMod(Lg[leg]);
                Lg[leg] = Lg[leg] + 0.1;
                return res;
            }
            else
                return 0.0;
            break;
        default:
            return 0.0;
            break;
        }
    }
}
