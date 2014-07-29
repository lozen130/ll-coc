#!/usr/bin/env python


def main():
	# Device name
	device_name = "sample"

	device = {}

	# Device specs
	device["_resolution"] = [1080, 1920]
	device["_clockwise"] = 3
	device["_counterclock"] = 1

	# Touch event
	device["_touch_event"] = "/dev/input/event1"

	# Cropping area
	device["_crop_area"] = "190x220+96+130"

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