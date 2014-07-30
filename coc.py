#!/usr/bin/env python
import os
import sys
import random
import time
import ast
import subprocess
import argparse

# Global variable
DEVICE = {}


def get_orientation():
	out = os.popen("adb shell dumpsys input | grep 'SurfaceOrientation' | awk '{ print $2 }'")
	for l in out:
		#print int(l.strip())
		return int(l.strip())


def get_resources():
	res = []

	f_name = "_coc"
	f_png = "%s.png" % f_name
	f_tiff = "%s.tiff" % f_name
	f_txt = "%s.txt" % f_name

	cmd_capture = "adb shell screencap -p /sdcard/%s" % f_png
	cmd_save = "adb pull /sdcard/%s ." % f_png

	degree = 0
	orientation = get_orientation()
	if orientation == DEVICE["_counterclock"]:
		degree = 270
	elif orientation == DEVICE["_clockwise"]:
		degree = 90
	else:
		return res
	cmd_rotate = "convert %s -rotate %d %s" % (f_png, degree, f_png)

	crop_area = DEVICE["_crop_area"]
	cmd_crop = "convert %s -crop %s -resize 400%% +contrast +contrast +contrast -brightness-contrast -64 -negate -type Grayscale %s" % (f_png, crop_area, f_tiff)

	cmd_ocr = "tesseract -l eng %s %s digit" % (f_tiff, f_name)

	os.system(cmd_capture)
	os.system(cmd_save)
	os.system(cmd_rotate)
	os.system(cmd_crop)
	os.system(cmd_ocr)

	resources = open(f_txt , 'r')
	for line in resources:
		if len(line.strip()) > 0:
			res.append(int(line.replace(' ', '').strip()))

	print res
	return res


def tap_attack():
	tap_XY(DEVICE["tap_attack"])


def tap_attack_close():
	tap_XY(DEVICE["tap_attack_close"])


def tap_attack_find():
	tap_XY(DEVICE["tap_attack_find"])


def tap_attack_next():
	tap_XY(DEVICE["tap_attack_next"])


def tap_attack_end():
	tap_XY(DEVICE["tap_attack_end"])


def tap_XY(coordinate):
	x = 0
	y = 0
	orientation = get_orientation()
	if orientation == DEVICE["_counterclock"]:
		x = coordinate[0]
		y = coordinate[1]
	elif orientation == DEVICE["_clockwise"]:
		x = DEVICE["_resolution"][0] - coordinate[0]
		y = DEVICE["_resolution"][1] - coordinate[1]
	else:
		return

	touch_event = DEVICE["_touch_event"]

	events = []
	events.append("%s 3 57 7736" % touch_event)
	events.append("%s 3 53 %d" % (touch_event, x))
	events.append("%s 3 54 %d" % (touch_event, y))
	events.append("%s 0 0 0" % touch_event)
	events.append("%s 3 57 4294967295" % touch_event)
	events.append("%s 0 0 0" % touch_event)
	send_events(events)


def send_events(events):
	for event in events:
		os.system("adb shell sendevent %s" % event)


def wait_for_a_while(start=30, end=60):
	wait_time = random.randint(start, end)
	time.sleep(wait_time)
	return wait_time


def threshold_reached(res, gold, ex, dark):
	if (res[0] > gold) or (res[1] > ex):
		return True
	elif (res[0] + res[1] > (gold + ex)*0.67):
		return True
	elif (len(res) == 4) and (res[2] > dark):
		return True
	else:
		return False


def search(delay=8, gold=120000, ex=120000, dark=1000, skip_ocr=False):
	print "\n[COC] Search Mode"

	print "Gold   threshold: {:7,d}".format(gold)
	print "Elixir threshold: {:7,d}".format(ex)
	print "Dark E threshold: {:7,d}".format(dark)
	print "Searching delay : %d seconds" % delay
	print "Parse loots: %s" % ("No" if skip_ocr else "Yes")

	count = 0
	print_timestamp(count)

	while True:
		count += 1
		tap_attack_next()

		# Loading...
		wait_for_a_while(delay, delay)

		# Processing...
		if skip_ocr:
			print_timestamp(count, wait_for_a_while(4, 6))

		else:
			res = get_resources()
			if (len(res) >= 2) and threshold_reached(res, gold, ex, dark):
				cmd_say = "say 'Gold %d, elixir %d. I found the target. Shall we attack now?'" % (res[0]/1000*1000, res[1]/1000*1000)
				os.system(cmd_say)
				print_timestamp(count, wait_for_a_while(1, 3))

			else:
				print_timestamp(count)


def attack():
	print "\n[COC] Attack Mode"

	cmd_1 = "adb shell am start -n com.supercell.clashofclans/.GameApp"
	cmd_2 = "adb shell am force-stop com.supercell.clashofclans"

	os.system(cmd_2)
	os.system(cmd_1)
	wait_for_a_while(20, 25)
	tap_attack()
	wait_for_a_while(2, 4)
	tap_attack_find()
		
#		tap_attack_end()
#		tap_attack_close()


def print_timestamp(count, delay=None):
	if delay == None:
		print "\n[%3d] %s" % (count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	else:
		print "\n[%3d] %s (+%2d seconds)" % (count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  delay)


def load_device_config(device="nexus_5"):
	global DEVICE
	print "Device: %s" % device

	with open("config/%s.config" % device, 'r') as f:
		s = f.read()
		DEVICE = ast.literal_eval(s)


def pre_processing(args):
	load_device_config(args.device)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='A simple COC attack planner.')
	parser.add_argument('-d', '--device', dest='device', choices=['nexus_5'], default='nexus_5', help='device name')
	parser.add_argument('-g', '--gold', dest='gold', default=150000, type=int, help='gold threshold')
	parser.add_argument('-e', '--elixir', dest='ex', default=150000, type=int, help='elixir threshold')
	parser.add_argument('-D', '--dark', dest='dark', default=1000, type=int, help='dark elixir threshold')
	parser.add_argument('--delay', dest='delay', default=8, type=int, help='searching delay')
	parser.add_argument('-a', '--attack', dest='attack', action='store_true', help='attack from main screen')
	parser.add_argument('-s', '--skip-ocr', dest='skip_ocr', action='store_true', help='skip parsing loots')
	args = parser.parse_args()

	pre_processing(args)

	if (args.attack):
		attack()

	search(delay=args.delay, gold=args.gold, ex=args.ex, dark=args.dark, skip_ocr=args.skip_ocr)
