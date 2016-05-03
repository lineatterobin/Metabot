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

#include "config.h"
#include "function.h"
#include "motion.h"
#include "moves.h"
#include "leds.h"
#include "kinematic.h"

float xMove[4], yMove[4], zMove[4];
float alpha[4], beta[4], Gamma[4];

bool helloMove(float t, float h, bool backLegs, float smoothBackLegs)
{
    float a, b, c;
//    Function X[4];
//    Function Y[4];
//    Function Z[4];
//    if (t == 0) {

//        X[0].addPoint(0.0, 90.0);
//        X[0].addPoint(50.0, 65.0);
//        X[0].addPoint(250.0, 65.0);
//        X[0].addPoint(300.0, 90.0);

//        X[1].addPoint(0.0, 90.0);
//        X[1].addPoint(50.0, 90.0);
//        X[1].addPoint(250.0, 90.0);
//        X[1].addPoint(300.0, 90.0);

//        X[2].addPoint(0.0, 90.0);
//        X[2].addPoint(50.0, 90.0);
//        X[2].addPoint(250.0, 90.0);
//        X[2].addPoint(300.0, 90.0);

//        X[3].addPoint(0.0, 90.0);
//        X[3].addPoint(50.0, 90.0);
//        X[3].addPoint(250.0, 90.0);
//        X[3].addPoint(300.0, 90.0);


//        Y[0].addPoint(0.0, 0.0);
//        Y[0].addPoint(50.0, 0.0);
//        Y[0].addPoint(250.0, 0.0);
//        Y[0].addPoint(300.0, 0.0);

//        Y[1].addPoint(0.0, 0.0);
//        Y[1].addPoint(10.0, 10.0);
//        Y[1].addPoint(290.0, 10.0);
//        Y[1].addPoint(300.0, 0.0);

//        Y[2].addPoint(0.0, 0.0);
//        Y[2].addPoint(10.0, 0.0);
//        Y[2].addPoint(290.0, 0.0);
//        Y[2].addPoint(300.0, 0.0);

//        Y[3].addPoint(0.0, 0.0);
//        Y[3].addPoint(10.0, -10.0);
//        Y[3].addPoint(290.0, -10.0);
//        Y[3].addPoint(300.0, 0.0);

//        Z[0].addPoint(0.0, h);
//        Z[0].addPoint(50.0, h+175.0);
//        Z[0].addPoint(250.0, h+175.0);
//        Z[0].addPoint(300.0, h);

//        Z[1].addPoint(0.0, h);
//        Z[1].addPoint(50.0, h);
//        Z[1].addPoint(250.0, h);
//        Z[1].addPoint(300.0, h);

//        Z[2].addPoint(0.0, h);
//        Z[2].addPoint(50.0, h);
//        Z[2].addPoint(250.0, h);
//        Z[2].addPoint(300.0, h);

//        Z[3].addPoint(0.0, h);
//        Z[3].addPoint(50.0, h);
//        Z[3].addPoint(250.0, h);
//        Z[3].addPoint(300.0, h);
//    }

    //Evolution du ouvement
    for (int i = 0; i < 4; i++)
    {
        // This is the x,y,z order in the referencial of the leg
        if(t==0)
        {
            xMove[i] = 90.0;
            yMove[i] = 0.0;
            zMove[i] = h;
        }

        switch (i) {
        case 0:
            if (t<50)
            {
                zMove[i] += 3.5;
                xMove[i] -= 0.5;
            }
            else if (t<75)
            {
                Gamma[i] = (t-50);
            }
            else if (t<125)
            {
                Gamma[i] = 25-(t-75);
            }
            else if (t<175)
            {
                Gamma[i] = -25+(t-125);
            }
            else if (t<225)
            {
                Gamma[i] = 25-(t-175);
            }
            else if (t<250)
            {
                Gamma[i] = -25+(t-225);
            }
            else if (t>250)
            {
                zMove[i] -= 3.5;
                xMove[i] += 0.5;
            }
            break;
        case 1:
            if (t<50)
                yMove[i] += 1;
            else if (t>250)
                yMove[i] -= 1;
            Gamma[i] = 0;
            break;
        case 2:
            break;
            Gamma[i] = 0;
        case 3:
            if (t<50)
                yMove[i] -= 1;
            else if (t>250)
                yMove[i] += 1;
            Gamma[i] = 0;
            break;
        }
        if (computeIK(xMove[i], yMove[i], zMove[i], &a, &b, &c, L1, L2, backLegs ? L3_2 : L3_1)) {
            l1[i] = -signs[0]*a + alpha[i];
            l2[i] = -signs[1]*b + beta[i];
            l3[i] = -signs[2]*(c - 180*smoothBackLegs) + Gamma[i];
        }
        else {
            led_set_all(LED_R, true);
        }
    }
    if(t == 300)
        return true;
    else
        return false;
}
