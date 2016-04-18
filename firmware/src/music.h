#ifndef _METABOT_MUSIC_H
#define _METABOT_MUSIC_H

float motion_music(int motor, int leg);
float calc_angle_perc(int motor, float freq, float phase);
float calc_angle_glide(int motor, float freq, float phase);
float calc_angle_scratch(int motor, float freq, float phase);

#endif

