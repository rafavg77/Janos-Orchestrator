# Janos-Orchestrator

Janos Orquestador was born from the need to constantly execute key tasks and on that result execute some other action. Janos is made up of two parts, the "client" and "server" part.

# Modules

#   DHCP Leases Monitor

The operation of this module is very limited to carry out a single activity but it can be modified to read any other log, event or even incorporate another type of monitoring by SNMP, SYSLOG, etc. Likewise, the functionality to send telegram messages to the designated Chat is centralized.

#   Client

The DHCP Leases Monitor module client has the ability to read the log file /var/log/pihole.log of a PiHole in search of DHCPACK events and in this way identify when a host connects to the network and accepts the offered IP address.

#   Server

The server exposes an enpoint in the path / monitor where it receives the ip, mac address and hostname parameters sent by the client, to perform a review in the database to identify if it is a new device or a device previously seen. At the end, send a telegram notification to report the identified activity.

![screen](https://raw.githubusercontent.com/rafavg77/Janos-Orchestrator/main/img/image_2021-11-13_17-48-55.png)

## TODO:
- [x] Read logs for DHCPACK events.
    - [x] Identify if it is a new device.
    - [x] If it is a previously viewed device, identify the last date the device was viewed.
- [ ] Document the installation steps.
- [ ] Perform integration with suricata IDS.
- [ ] Perform integration with automatic consultation of electricity, water and gas bills.
- [ ] Integrate users, roles, authorization and authentication-
- [ ] Run other nerdy tasks.