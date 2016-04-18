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

#include "kinematic.h"
#include "music.h"

TERMINAL_PARAMETER_FLOAT(freqLeg1, "Leg 1's freq", 0.0);
TERMINAL_PARAMETER_FLOAT(freqLeg2, "Leg 2's freq", 0.0);
TERMINAL_PARAMETER_FLOAT(freqLeg3, "Leg 3's freq", 0.0);
TERMINAL_PARAMETER_FLOAT(freqLeg4, "Leg 4's freq", 0.0);

#define MODE_PERC       0
#define MODE_GLIDE      1
#define MODE_SCRATCH    2

TERMINAL_PARAMETER_INT(modeLeg1, "Mode (0:Perc, 1:TODO)", MODE_PERC);
TERMINAL_PARAMETER_INT(modeLeg2, "Mode (0:Perc, 1:TODO)", MODE_PERC);
TERMINAL_PARAMETER_INT(modeLeg3, "Mode (0:Perc, 1:TODO)", MODE_PERC);
TERMINAL_PARAMETER_INT(modeLeg4, "Mode (0:Perc, 1:TODO)", MODE_PERC);

TERMINAL_PARAMETER_FLOAT(phaseLeg1, "Leg 1's phase", 0.5);
TERMINAL_PARAMETER_FLOAT(phaseLeg2, "Leg 2's phase", 0.0);
TERMINAL_PARAMETER_FLOAT(phaseLeg3, "Leg 3's phase", 0.5);
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

#define TMAX 10000
float tps = 0;

float motion_music(int motor, int leg) {

    float freq;
    float phase;
    int mode;

    tps++;
    if (tps > TMAX) {
        tps -= TMAX;
    }
    if (tps < 0.0) tps++;

    switch(leg) {
    case 0:
        phase = phaseLeg1;
        freq = freqLeg1;
        mode = modeLeg1;
        break;
    case 1:
        phase = phaseLeg2;
        freq = freqLeg2;
        mode = modeLeg2;
        break;
    case 2:
        phase = phaseLeg3;
        freq = freqLeg3;
        mode = modeLeg3;
        break;
    case 3:
        phase = phaseLeg4;
        freq = freqLeg4;
        mode = modeLeg4;
        break;
    default:
        freq = 0;
        mode = MODE_PERC;
        break;
    }

    switch(mode) { //Add more modes in this switch
    case MODE_PERC:
        return calc_angle_perc(motor, freq, phase);
        break;
    case MODE_GLIDE:
        return calc_angle_glide(motor, freq, phase);
        break;
    case MODE_SCRATCH:
        return calc_angle_scratch(motor, freq, phase);
        break;
    default:
        return 0.0;
        break;
    }


}

//Mode Perc calculation
float calc_angle_perc(int motor, float freq, float phase) {
    float time;
    switch(motor) {
    case 1:
        return 0.0;
        break;
    case 2:
        time = fmod((freq*tps)/(TMAX*1.0),1)*3.14;
        time += phase*3.14;
        return (abs(sin(time))-abs(cos(time-3.14/2.5))+0.3)*30.0;
        break;
    case 3:
        return 0.0;
        break;
    default:
        return 0.0;
        break;
    }
}

//Mode Glide calculation
float calc_angle_glide(int motor, float freq, float phase) {
    float time;
    switch(motor) {
    case 1:
        return 0.0;
        break;
    case 2:
        time = fmod((freq*tps)/(TMAX*1.0),1)*3.14;
        time += phase*3.14;
        return ((abs(cos(time)))-1)*50.0;
        break;
    case 3:
        time = fmod((freq*tps)/(TMAX*1.0),1)*3.14;
        time += phase*3.14;
        return ((abs(cos(time)))-1)*50.0;
        break;
    default:
        return 0.0;
        break;
    }
}

//Mode Scratch calculation
float calc_angle_scratch(int motor, float freq, float phase) {
    float time;
    float result;
    switch(motor) {
    case 1:
        return 0.0;
        break;
    case 2:
        time = fmod((freq*tps)/(TMAX*1.0),1)*3.14;
        time += phase*3.14;
        result = (sin(time)-1);
        if(result > -1)
            return result*50.0;
        else
            return 0.0;
        break;
    case 3:
        time = fmod((freq*tps)/(TMAX*1.0),1)*3.14;
        time += phase*3.14;
        result = (sin(time)-1);
        if(result > -1)
            return result*50.0;
        else
            return 0.0;
        break;
    default:
        return 0.0;
        break;
    }
}

