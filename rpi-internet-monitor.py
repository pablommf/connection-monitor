#!/usr/bin/env python
#original idea:https://www.instructables.com/Raspberry-Pi-Internet-Monitor/

import subprocess
import sys
import time
import RPi.GPIO as GPIO

GPIO_SHUTDOWN_SWITCH = 24  # switch for shutdown
GPIO_SHUTDOWN_LED = 23     # led for indicating raspberry pi connected

DELAY_BETWEEN_PINGS = 1    # delay in seconds
DELAY_BETWEEN_TESTS = 120  # delay in seconds

SITES = ["google.com", "amazon.com", "cloudflare.com"]

# print messages for debugging when indicator is set
def debug_message(debug_indicator, output_message):
  if debug_indicator:
    print output_message

# issue Linux ping command to determine internet connection status
def ping(site):
  cmd = "/bin/ping -c 1 " + site
  try:
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
  except subprocess.CalledProcessError, e:
    debug_message(debug, site + ": not reachable")
    return 0
  else:
    debug_message(debug, site + ": reachable")
    return 1

# ping the sites in the site list the specified number of times
# and calculate the percentage of successful pings
def ping_sites(site_list, wait_time, times):
  successful_pings = 0
  attempted_pings = times * len(site_list)
  for t in range(0, times):
    for s in site_list:
      successful_pings += ping(s)
      time.sleep(wait_time)
  debug_message(debug, "Percentage successful: " + str(int(100 * (successful_pings / float(attempted_pings)))) + "%")
  return successful_pings / float(attempted_pings)   # return percentage successful 

      
# main program starts here

# check to see if the user wants to print debugging messages
debug = False
if len(sys.argv) > 1:
  if sys.argv[1] == "-debug":
    debug = True
  else:
    print "unknown option specified: " + sys.argv[1]
    sys.exit(1)

# setup the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_SHUTDOWN_LED, GPIO.OUT)
GPIO.setup(GPIO_SHUTDOWN_SWITCH, GPIO.OUT)

# main loop: ping sites, turn appropriate lamp on, wait, repeat
test = 0
while True:
  test+=1
  debug_message(debug, "----- Test " + str(test) + " -----")
  success = ping_sites(SITES, DELAY_BETWEEN_PINGS, 2)
  if success == 0:
    lamp_red_on()
  elif success <= .50:  
    lamp_amber_on()
  else:
    lamp_green_on()
  debug_message(debug, "Waiting " + str(DELAY_BETWEEN_TESTS) + " seconds until next test.")
  time.sleep(DELAY_BETWEEN_TESTS)
