#!/usr/bin/env python3
import fluidsynth, time

channel = 0
currSF2Path = "/home/pi/GeneralUser GS 1.47/GeneralUser GS v1.47.sf2"
currPatchName = ""
currBank = 0
currPatch = 0
bankpatchlist = []

### SF2 Handling Setup ###
from sf2utils.sf2parse import Sf2File

def setSF2bankpatchlist(sf2path: str):
	"""
	Gets a nested list of the banks and patches in use by the soundfont
	(yes it's a horribly nested one liner, but it works)
	"""
	with open(sf2path, 'rb') as sf2_file:
		sf2 = Sf2File(sf2_file)

	return([[int(i[0]), int(i[1])] for i in [i.split(":") for i in sorted([i[7:14] for i in str(sf2.presets)[1:-1].split(", ")])[:-1]]])


### SF2 Handling Setup End ####

### FluidSynth Setup ###
fs = fluidsynth.Synth()
fs.setting('synth.polyphony', 32)
fs.setting('audio.period-size', 6)
fs.setting('audio.periods', 4)
fs.setting('audio.realtime-prio', 99)

fs.start(driver='alsa', device='hw:Device,0', midi_driver='alsa_seq')

sfid = fs.sfload(currSF2Path)
fs.program_select(0, sfid, 0, 0)	

def patchInc(channel: int, bankpatchlist):
	'''
	Finds next non empty patch, moving to the next bank if needs be.
	Max bank 128 before it loops around to 0.
	'''
	global currPatchName
	global currBank
	global currPatch
	currBank = fs.channel_info(channel)[1]
	currPatch = fs.channel_info(channel)[2]
	currIndex = bankpatchlist.index([currBank, currPatch])

	if (currIndex + 1) == len(bankpatchlist):
		currIndex = 0
	else:
		currIndex += 1
	[currBank, currPatch] = bankpatchlist[currIndex]
	fs.program_select(channel, sfid, currBank, currPatch)
	currPatchName = fs.channel_info(channel)[3].decode("utf-8")
	print(fs.channel_info(channel))

def patchDec(channel: int, bankpatchlist):
	'''
	Finds previous non empty patch, moving to the previous bank if needs be.
	Max bank 128 after looping around from 0.
	'''
	global currPatchName
	global currBank
	global currPatch
	currBank = fs.channel_info(channel)[1]
	currPatch = fs.channel_info(channel)[2]
	currIndex = bankpatchlist.index([currBank, currPatch])

	if (currIndex - 1) == -1:
		currIndex = len(bankpatchlist) - 1
	else:
		currIndex -= 1
	[currBank, currPatch] = bankpatchlist[currIndex]
	fs.program_select(channel, sfid, currBank, currPatch)
	currPatchName = fs.channel_info(channel)[3].decode("utf-8")
	print(fs.channel_info(channel))

### End FluidSynth Setup ###

### LCD Setup ###
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

lcd = CharLCD(pin_rs=22, pin_e=23, pins_data=[9, 25, 11, 8], cols=16, rows=2, numbering_mode=GPIO.BCM)
#GPIO.BOARD: pin_rs=15, pin_e=16, pins_data=[21, 22, 23, 24]

def writeLCD(firstline: str, secondline: str):
	'''
	Writes 2 lines to a 16x2 LCD
	Shortens them by removing vowels if needed
	'''
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
		patchInc(channel, bankpatchlist)
		writeLCD(currPatchName, 'Bank ' + str(currBank) + ' Patch ' + str(currPatch))

def my_deccallback(scale_position):
	if scale_position%2 == 0:
		patchDec(channel, bankpatchlist)
		writeLCD(currPatchName, 'Bank ' + str(currBank) + ' Patch ' + str(currPatch))

def my_swcallback():
	return

my_encoder = pyky040.Encoder(CLK=17, DT=18, SW=27)
#GPIO.BOARD: CLK=11, DT=12, SW=13


my_encoder.setup(scale_min=1, scale_max=100, step=1, loop=True, inc_callback=my_inccallback, dec_callback=my_deccallback, sw_callback=my_swcallback)


### End Rotary Encoder Setup ###

bankpatchlist = getsf2bankpatchlist(currSF2Path)

currPatchName = fs.channel_info(channel)[3].decode("utf-8")
writeLCD(currPatchName, 'Bank ' + str(currBank) + ' Patch ' + str(currPatch))

my_encoder.watch()

'''
while True:
	time.sleep(2)
	patchInc()
	lcd.clear()
	writeLCD(currPatchName, 'Bank ' + str(currBank) + ' Patch ' + str(currPatch))
'''
