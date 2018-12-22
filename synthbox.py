#!/usr/bin/env python3
import fluidsynth, time

currPatchName = ""
currBank = 0
currPatch = 0

### FluidSynth Setup ###
fs = fluidsynth.Synth()
fs.setting('synth.polyphony', 32)
fs.setting('audio.period-size', 6)
fs.setting('audio.periods', 4)
fs.setting('audio.realtime-prio', 99)

fs.start(driver='alsa', device='hw:Device,0', midi_driver='alsa_seq')

sfid = fs.sfload('/home/pi/GeneralUser GS 1.47/GeneralUser GS v1.47.sf2')
fs.program_select(0, sfid, 0, 0)

def patchInc():
	global currPatchName
	global currBank
	global currPatch
	currBank = fs.channel_info(0)[1]
	currPatch = fs.channel_info(0)[2] + 1
	while True:
		if fs.program_select(0, sfid, currBank, currPatch) == -1:
			if currPatch == 128:
				currPatch = 0
				currBank += 1
				if currBank == 128: #16384:
						currBank = 0
			else:
				currPatch += 1
		else:
			currPatchName = fs.channel_info(0)[3].decode("utf-8")
			print(fs.channel_info(0))
			break

def patchDec():
	global currPatchName
	global currBank
	global currPatch
	currBank = fs.channel_info(0)[1]
	currPatch = fs.channel_info(0)[2] - 1
	while True:
		if fs.program_select(0, sfid, currBank, currPatch) == -1:
			if currPatch == -1:
				currPatch = 127
				currBank -= 1
				if currBank == -1:
					currBank = 127 #16383
			else:
				currPatch -= 1
		else:
			currPatchName = fs.channel_info(0)[3].decode("utf-8")
			print(fs.channel_info(0))
			break

### End FluidSynth Setup ###

### LCD Setup ###
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

lcd = CharLCD(pin_rs=22, pin_e=23, pins_data=[9, 25, 11, 8], cols=16, rows=2, numbering_mode=GPIO.BCM)

def writeLCD(firstline: str, secondline: str):
	lcd.clear()
	if len(firstline) > 16:
		for i in ['a','e','i','o','u']:
			firstline = firstline.replace(i, '')
		if len(firstline) > 16:
			firstline = firstline[0:16]
	
	if len(secondline) > 16:
		for i in ['a','e','i','o','u']:
			secondline = secondline.replace(i, '')
		if len(secondline) > 16:
			secondline = secondline[0:16]
	lcd.write_string(firstline + '\n\r' + secondline)

### End LCD Setup ###

### Rotary Encoder Setup ###
from pyky040 import pyky040

def my_inccallback(scale_position):
	if scale_position%2 == 0:
		patchInc()
		writeLCD(currPatchName, 'Bank ' + str(currBank) + ' Patch ' + str(currPatch))

def my_deccallback(scale_position):
	if scale_position%2 == 0:
		patchDec()
		writeLCD(currPatchName, 'Bank ' + str(currBank) + ' Patch ' + str(currPatch))

def my_swcallback():
	return

my_encoder = pyky040.Encoder(CLK=17, DT=18, SW=27)

my_encoder.setup(scale_min=1, scale_max=100, step=1, loop=True, inc_callback=my_inccallback, dec_callback=my_deccallback, sw_callback=my_swcallback)


### End Rotary Encoder Setup ###



#print(fs.channel_info(0))
#fs.program_select(0, sfid, 0, 127)
print(fs.channel_info(0))

writeLCD(currPatchName, 'Bank ' + str(currBank) + ' Patch ' + str(currPatch))

my_encoder.watch()

'''
while True:
	time.sleep(2)
	patchInc()
	lcd.clear()
	writeLCD(currPatchName, 'Bank ' + str(currBank) + ' Patch ' + str(currPatch))
'''
