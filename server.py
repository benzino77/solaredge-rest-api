#!/usr/bin/env python3

from os import getenv
import solaredge_modbus
from flask import Flask, jsonify, request

inverter = solaredge_modbus.Inverter(
    host=getenv('MODBUS_HOST'),
    port=getenv('MODBUS_PORT'),
    timeout=5,
    unit=1
)


error_message = {'succes': False, 'data': {'error': 'Not allowed.'}}

app = Flask(__name__)


@app.route('/api/v1/solaredge', methods=['GET', 'POST', 'PUT', 'DELETE'])
def metrics_api():
    if request.method != 'GET':
        return jsonify(error_message), 405

    values = {}
    
    num_of_tries = 5
    while num_of_tries > 0:
        try:
            values = inverter.read_all()
            meters = inverter.meters()
            batteries = inverter.batteries()
            break
        except Exception as e:
            print('Something went wrong: {e}')

    values['meters'] = {}
    values['batteries'] = {}

    for meter, params in meters.items():
        meter_values = params.read_all()
        values['meters'][meter] = meter_values

    for battery, params in batteries.items():
        battery_values = params.read_all()
        values['batteries'][battery] = battery_values

    ret_val = {}
    ret_val['success'] = True
    ret_val['data'] = values
    return jsonify(ret_val)


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    return jsonify(error_message), 405
