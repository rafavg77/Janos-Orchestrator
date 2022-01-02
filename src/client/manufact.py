# -*- coding: utf-8 -*-
from mac_vendor_lookup import MacLookup

mac = MacLookup()
mac.update_vendors() 


def find_mac(mac_address):
    try:
        find = mac.lookup(mac_address)    
    except Exception:
        find = "No Definido"
        pass
    print(find)
#print(MacLookup().lookup("D6:19:9F:E0:90:B1"))

find_mac("20:0B:CF:E3:8F:49")
#find_mac("D6:19:9F:E0:90:B1")