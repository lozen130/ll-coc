#!/usr/bin/env python


def main():
	# Device name
	device_name = "sample"

	device = {}

	# Touch event
	device["_touch_event"] = "/dev/input/event1"

	# Cropping area
	device["_crop_area"] = "220x190+730+96"

	# Coordinates
	device["tap_attack"] = [131, 149]
	device["tap_attack_close"] = [983, 1853]
	device["tap_attack_find"] = [255, 420]
	device["tap_attack_next"] = [341, 1698]
	device["tap_attack_end"] = [308, 154]

	with open ("config/%s.config" % device_name, 'w') as f:
		f.write(str(device))

	print device


if __name__ == "__main__":
	main()