# -*- coding: utf-8 -*-

# import main Flask class and request object
from flask import Flask, request, jsonify
import db.databaseHelper as databaseHelper
import bot.sendToTelegram as sendToTelegram

# create the Flask app
app = Flask(__name__)

@app.route('/')
def query_example():
    response_body = {
            "message": "Welcome to Monitor Leases!"
            }

    return jsonify(response_body)

@app.errorhandler(404)
def page_not_found(e):
    response_body = {
            "message": "Not Found :("
            }

    return jsonify(response_body), 404

@app.route('/monitor', methods=['POST'])
def monitor():
    request_data = request.get_json()
    ip = request_data['ip']
    mac = request_data['mac']
    hostname = request_data['hostname']
    lastDetected, minutes, status, isNew = databaseHelper.getLastDetected(mac)
    if isNew:
        sendToTelegram.sendMessage("[+] Se dectecto un nuevo dispotivo {} - {} - {}".format(ip,mac,hostname))
        databaseHelper.intert2History(ip,mac,hostname)
    else: 
        if status:
            databaseHelper.intert2History(ip,mac,hostname)
            print("Se detectó dispositivo con más de 1 hora {} - {} - {}".format(ip,mac,hostname))
            sendToTelegram.sendMessage("[+] Se dectecto el dispotivo {} - {} - {} ultima vez detectado {}".format(ip,mac,hostname,lastDetected))
        else:
            databaseHelper.intert2History(ip,mac,hostname)
            print("El dipositivo  {} - {} - {} tiene menos del tiempo definido".format(ip,mac,hostname))

    response_body = {
            "message": "Successfull",
            "ip":ip
            }
    return jsonify(response_body)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5000)
