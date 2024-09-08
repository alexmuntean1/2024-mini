#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(0.5)


def quiet():
    speaker.duty_u16(0)


freq: float = 30
duration: float = 0.1  # seconds

playtone(392, 1) #G
playtone(440, 1) #A
playtone(392, 1) #G
playtone(523, 1) #C
playtone(493, 1) #B
playtone(392, 1) #G
playtone(440, 1) #A
playtone(392, 1) #G
playtone(587, 1) #D
playtone(523, 1) #C
playtone(392, 1) #G
playtone(783, 1) #highG
playtone(659, 1) #E
playtone(523, 1) #C
playtone(493, 1) #B
playtone(440, 1) #A
playtone(698, 1) #F
playtone(659, 1) #E
playtone(523, 1) #C
playtone(587, 1) #D
playtone(523, 1) #C
quiet()

# Turn off the PWM
quiet()
