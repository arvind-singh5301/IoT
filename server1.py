
import time
import sys
import json
import pprint
import uuid
from uuid import getnode as get_mac


try:
	import ibmiotf.application
	import ibmiotf.device
except ImportError:
	# This part is only required to run the sample from within the samples
	# directory when the module itself is not installed.
	#
	# If you have the module installed, just use "import ibmiotf.application" & "import ibmiotf.device"
	import os
	import inspect
	cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
	if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
	import ibmiotf.application
	import ibmiotf.device


def myAppEventCallback(event):
	y=0
	while(y<1):
		print("Received live data from %s (%s) sent at %s: %s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), json.dumps(event.data)))
		y=y+1

#####################################
#FILL IN THESE DETAILS
#####################################     
organization = "ihd64f"
deviceType = "RaspberryPi"
deviceId = "b827eb42b125"
appId = str(uuid.uuid4())
authMethod = "token"
authToken = "aRdqQAEaq&u+YN2PYw"

##API TOKEN AND KEY
authkey = "a-ihd64f-0ewoxrypp7"
authtoken = "K*B9YI7E7@vGUJh!J5"
# Initialize the application client.

try:
	appOptions = {"org": organization, "id": appId,"auth-method": "apikey", "auth-key" : authkey, "auth-token":authtoken }
	

except Exception as e:
	print(str(e))
	sys.exit()

# Connect and configuration the application
# - subscribe to live data from the device we created, specifically to "greeting" events
# - use the myAppEventCallback method to process events
while(True):
	command = raw_input("Enter the command: ")

	if command == 'lighton':
		print "Turning Light ON"
		command = 'null'
		try:
			appCli = ibmiotf.application.Client(appOptions)
			appCli.connect()
			commandData={'LightON' : 1}
		
			appCli.publishCommand(deviceType, deviceId, "on", commandData)
			appCli.publishEvent(deviceType, deviceId,"status",commandData)
			x=0
			while(x<1):
				appCli.deviceEventCallback = myAppEventCallback
				appCli.subscribeToDeviceEvents(event="status")
				print "testing"
				x=x+1
				time.sleep(1)

		
			
		except Exception as e:
			print ("Connect attempt failed: "+str(e))
			sys.exit()


	if command == 'lightoff':
		print "Turning Light OFF"
		try:
			appCli = ibmiotf.application.Client(appOptions)
			appCli.connect()
			commandData={'LightOFF' : 0}
		
			appCli.publishCommand(deviceType, deviceId, "off", commandData)
			appCli.publishEvent(deviceType, deviceId,"status",commandData)
			while(1):
				appCli.deviceEventCallback = myAppEventCallback
				appCli.subscribeToDeviceEvents(event="status")
		
			
		except Exception as e:
			print ("Connect attempt failed: "+str(e))
			sys.exit()

appCli.disconnect()

