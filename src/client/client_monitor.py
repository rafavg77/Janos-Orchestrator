#from pushbullet import Pushbullet
import requests

def sendRequest(ip,mac, hostname):
    r = requests.post('http://192.168.90.210:5000/monitor', json={"ip":ip,"mac":mac,"hostname":hostname})
    print(r.status_code)
    print(r.content)

process = subprocess.Popen(['tail','-f','/var/log/pihole.log'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    output = process.stdout.readline()
    #print(output.strip())
    if 'DHCPACK' in output.strip():
        if 'Archer_C1200' not in output.strip():
            print("Se encontró DHCPACK")
            ip = output.split()[5]
            mac = output.split()[6]
            name = output.split()[7]
            print(ip)
            print(mac)
            print(name)
            #push = pb.push_note("DNS Notification", "Dispositivo conectado: " + name)
            sendRequest(ip,mac,name)
    # Do something else
    return_code = process.poll()
    if return_code is not None:
        print('RETURN CODE', return_code)
        # Process has finished, read rest of the output 
        for output in process.stdout.readlines():
            print(output.strip())
        break
