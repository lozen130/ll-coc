#!/usr/bin/env python
import os
import sys
import subprocess


def main():
	print "Read from adb"
	# proc1 = subprocess.Popen("adb shell getevent".split(), stdout=subprocess.PIPE)
	# proc2 = subprocess.Popen("grep event1".split(), stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# proc1.stdout.close()
	# out, err = proc2.communicate()

	# for line in out.split('\n'):
	# 	print line

	event = "event1"

	output = os.popen("adb shell getevent | grep %s" % event)
	for line in output:
		elements = line.split()
		if elements[0].startswith("/dev/input/%s" % event):
			elements[1] = str(int(elements[1], 16))
			elements[2] = str(int(elements[2], 16))
			elements[3] = str(int(elements[3], 16))

		print ' '.join(elements)


if __name__ == "__main__":
	main()