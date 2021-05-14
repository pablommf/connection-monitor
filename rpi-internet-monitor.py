#!/usr/bin/env python
#original idea:https://www.instructables.com/Raspberry-Pi-Internet-Monitor/

import subprocess
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)


GPIO_MODEM = 4  # switch for shutdown
GPIO_CHANNEL1 = 22     # led for indicating raspberry pi connected
GPIO_CHANNEL2 = 6     # led for indicating raspberry pi connected
GPIO_CHANNEL3 = 26     # led for indicating raspberry pi connected

# setup the GPIO pins
GPIO.setup(GPIO_MODEM, GPIO.OUT)
GPIO.setup(GPIO_CHANNEL1, GPIO.OUT)
GPIO.setup(GPIO_CHANNEL2, GPIO.OUT)
GPIO.setup(GPIO_CHANNEL3, GPIO.OUT)


DELAY_BETWEEN_PINGS = 1    # delay in seconds
DELAY_BETWEEN_TESTS = 5  # delay in seconds

SITES = ["google.com", "amazon.com", "cloudflare.com"]


# print messages for debugging when indicator is set
def debug_message(debug_indicator, output_message):
  if debug_indicator:
    print (output_message)

# issue Linux ping command to determine internet connection status
def ping(site):
  cmd = "/bin/ping -c 1 " + site
  try:
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
  except subprocess.CalledProcessError:
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

      

def reset(channel):
   GPIO.output(channel, True)
   time.sleep(0.5)
   GPIO.output(channel, False)
return 1


# main program starts here

# check to see if the user wants to print debugging messages
debug = True

# main loop: ping sites, turn appropriate lamp on, wait, repeat
test = 0
while True:
  test+=1
  debug_message(debug, "----- Test " + str(test) + " -----")
  success = ping_sites(SITES, DELAY_BETWEEN_PINGS, 2)
  if success <= .50:
    reset(GPIO_MODEM)
  else:
    print "Connection OK"
  debug_message(debug, "Waiting " + str(DELAY_BETWEEN_TESTS) + " seconds until next test.")
  time.sleep(DELAY_BETWEEN_TESTS)
