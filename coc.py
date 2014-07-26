#!/usr/bin/env python
import os
import sys
import random
import time

adb = "/Users/becky/Downloads/adt-bundle-mac-x86_64-20140321/sdk/platform-tools/adb"

cmd_1 = "%s shell am start -n com.supercell.clashofclans/.GameApp" % adb
cmd_2 = "%s shell am force-stop com.supercell.clashofclans" % adb



def get_resources():
	f_name = "_coc"
	f_png = "%s.png" % f_name
	f_tiff = "%s.tiff" % f_name
	f_txt = "%s.txt" % f_name

	cmd_capture = "%s shell screencap -p /sdcard/lozen130/%s" % (adb, f_png)
	cmd_save = "%s pull /sdcard/lozen130/%s ." % (adb, f_png)
	cmd_crop = "convert %s -crop 90x240+855+99 -rotate 270 -resize 400%% -brightness-contrast -80 -type Grayscale %s" % (f_png, f_tiff)
	cmd_ocr = "tesseract -l eng %s %s nobatch digit" % (f_tiff, f_name)

#	print "Capturing..."
	os.system(cmd_capture)

#	print "Saving..."
	os.system(cmd_save)

#	print "Converting..."
	os.system(cmd_crop)

#	print "Reading..."
	os.system(cmd_ocr)

	resources = open(f_txt , 'r')

	res = []
	for line in resources:
		if len(line.strip()) > 0:
			res.append(int(line.replace(' ', '').strip()))

	print res
	return res


def tap_attack():
	tap_XY(131, 149)


def tap_attack_close():
	tap_XY(983, 1853)


def tap_attack_find():
	tap_XY(255, 420)


def tap_attack_next():
	tap_XY(341, 1698)


def tap_attack_end():
	tap_XY(308, 154)


def tap_XY(x, y):
	event_1 = "/dev/input/event1 3 57 7736"
	event_2 = "/dev/input/event1 3 53 %d" % x
	event_3 = "/dev/input/event1 3 54 %d" % y
	event_4 = "/dev/input/event1 0 0 0"
	event_5 = "/dev/input/event1 3 57 4294967295"
	event_6 = "/dev/input/event1 0 0 0"

	send_event(event_1, event_2, event_3, event_4, event_5, event_6)


def send_event(e_1, e_2, e_3, e_4, e_5, e_6):
	os.system("%s shell sendevent %s" % (adb, e_1))
	os.system("%s shell sendevent %s" % (adb, e_2))
	os.system("%s shell sendevent %s" % (adb, e_3))
	os.system("%s shell sendevent %s" % (adb, e_4))
	os.system("%s shell sendevent %s" % (adb, e_5))
	os.system("%s shell sendevent %s" % (adb, e_6))


def wait_for_a_while(start=30, end=60):
	wait_time = random.randint(start, end)
	time.sleep(wait_time)
	return wait_time


def threshold_reached(res, gold, ex):
	if (res[0] > gold) or (res[1] > ex):
		return True
	elif (res[0] + res[1] > (gold + ex)*0.67):
		return True
	else:
		return False


def smart_search(delay=8, gold=150000, ex=150000):
	print "[COC] Smart Search"
	print "Gold   threshold: %d" % gold
	print "Elixir threshold: %d" % ex
	print "Searching delay: %d" % delay

	count = 0
	print "\n[%3d] %s" % (count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

	while True:
		count += 1
		tap_attack_next()

		# Loading...
		wait_for_a_while(delay, delay)

		# Processing...
		res = get_resources()
		if (len(res) == 2) and threshold_reached(res, gold, ex):
			cmd_say = "say 'Gold %d, elixir %d. General, I found the target. Shall we attack now?'" % (res[0], res[1])
			os.system(cmd_say)
			print "\n[%3d] %s (+%2d sec)" % (count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  wait_for_a_while(1, 3))

		else:
			print "\n[%3d] %s" % (count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))



def fast_search():
	print "[COC] Fast Search"
	count = 0
	while True:
		count += 1
		wait_for_a_while(5, 5)
		get_resources()
		print "Processed"
		print "[%3d] %s (+%2d sec)" % (count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  wait_for_a_while(5, 7) + 5)
		tap_attack_next()


def searching_mode():
	print "[COC] Searching Mode"
	os.system(cmd_2)
	os.system(cmd_1)
	wait_for_a_while(20, 25)
	tap_attack()
	wait_for_a_while(2, 4)
	tap_attack_find()
		
	count = 0
	print "[%3d] %s" % (count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	while True:
		count += 1
		print "[%3d] %s (+%2d sec)" % (count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  wait_for_a_while(8, 12))
		tap_attack_next()
#		tap_attack_end()
#		tap_attack_close()


if __name__ == "__main__":
#	searching_mode()
#	fast_search()
	smart_search()

