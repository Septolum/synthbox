# synthbox
My Rasperry Pi Fluidsynth Box Project

Running on  a Pi Zero, with a 16x2 LCD Display and a single rotary encoder as an interface

Ran on a Pi with [AutoAconnect](https://github.com/Septolum/AutoAconnect) running in the background

Best results achieved when run as superuser

Crontab friendly command: `sudo su -c 'sudo -E python3 /home/pi/synthbox/synthbox.py' pi`

Depends on:
- pyFluidSynth
- sf2utils
- RPLCD
- RPi.GPIO
- pyky040

--------

Licenced under a [Creative Commons Attribution-Noncommercial-Share Alike 3.0 License](http://creativecommons.org/licenses/by-nc-sa/3.0/)
