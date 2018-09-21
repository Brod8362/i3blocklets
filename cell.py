import os
import sys
import json

num = os.popen(f'mmcli -L').read()
num = int(num.split("/")[-1].split(" ")[0])


ev = os.popen(f'mmcli -m {num}').read()


signal = os.popen(f'echo "{ev}" | grep "signal quality"').read()
carrier = os.popen(f'echo "{ev}" | grep "operator name"').read()
network_type = os.popen(f'echo "{ev}" | grep "access tech"').read()
power_state = os.popen(f'echo "{ev}" | grep "power state"').read()
state = os.popen(f'echo "{ev}" | grep "state"').read()
sim = os.popen(f'echo "{ev}" | grep "path"').read()


try:
    signal = int(signal.strip().split("'")[1])
    network_type = network_type.strip().split("'")[1].upper()
    power_state = power_state.strip().split("'")[1].lower()
    state = state.strip().split("'")[1].lower()
    sim = sim.strip().split("'")[1].lower()
except Exception as exc: # OO
    cellular = {'name':'cellular', 'color':'#FF0000', 'markup':'none', 'full_text':'Error!'} 
    json.dump(cellular, sys.stdout)
    sys.exit()

if state == "disabled": #for when it be off
	cellular = {'name':'cellular', 'color':'#29292B', 'markup':'none', 'full_text':'WWAN Disabled'}
	json.dump(cellular, sys.stdout)
	sys.exit()
if sim == "none": #for when sim not be
    cellular = {'name':'cellular', 'color':'#FFFFFF', 'markup':'none', 'full_text':'No SIM'}
    json.dump(cellular, sys.stdout)
    sys.exit()
if signal == 0 and state == "disconnected": #for when signal not be 
    cellular = {'name':'cellular', 'color':'#FF0000', 'markup':'none', 'full_text':'No Service'}
    json.dump(cellular, sys.stdout)
    sys.exit()
if state == "disconnected": #for when yer not connected
	cellular = {'name':'cellular', 'color':'#FF0000', 'markup':'none', 'full_text':'WWAN Disconnected'}
	json.dump(cellular, sys.stdout)
	sys.exit()

if signal >= 50: #good signal
	color = "#00FF00"
elif signal > 25 and signal < 50: #meh signal 
	color = "#FFFF00"
else: #bad signal 
	color = "#FF7700"

carrier = carrier.strip().split("'")[1]
final = f"WWAN {carrier} {signal}% ({network_type})"
cellular = {'name':'cellular', 'color':color, 'markup':'none', 'full_text':final}
json.dump(cellular, sys.stdout, separators=(',',':'))

