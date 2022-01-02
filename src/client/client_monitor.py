#from pushbullet import Pushbullet
import requests
import subprocess
from mac_vendor_lookup import MacLookup

def sendRequest(ip,mac, hostname):
    r = requests.post('http://192.168.90.210:5000/monitor', json={"ip":ip,"mac":mac,"hostname":hostname})
    print(r.status_code)
    print(r.content)

def find_mac(mac_address):
    mac = MacLookup()
    mac.update_vendors()
    try:
        find = mac.lookup(mac_address)    
    except Exception:
        find = "No Definido"
        pass
    print(find)
    return find

process = subprocess.Popen(['tail','-f','/var/log/pihole.log'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    output = process.stdout.readline()
    #print(output.strip())
    if 'DHCPACK' in output.strip():
        if 'Archer_C1200' not in output.strip():
            print("Se encontró DHCPACK")
            print(output)
            ip = output.split()[5]
            mac = output.split()[6]
            try:
                name = output.split()[7]
            except IndexError:
                name = find_mac(mac)
            print(ip)
            print(mac)
            print(name)
            
            sendRequest(ip,mac,name)
    # Do something else
    return_code = process.poll()
    if return_code is not None:
        print('RETURN CODE', return_code)
        # Process has finished, read rest of the output 
        for output in process.stdout.readlines():
            print(output.strip())
        break