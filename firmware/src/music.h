#ifndef _METABOT_MUSIC_H
#define _METABOT_MUSIC_H

float motion_music(int motor, int leg, float freq);

//OBSOLETE
//float calc_angle_perc(int motor, float freqLeg, float phase);
//float calc_angle_glide(int motor, float freqLeg, float phase);
float calc_angle_scratch(int motor, float freqLeg, float phase);

#endif

