# -*- coding: utf-8 -*-
import webbrowser
from datetime import datetime

from flask import Flask, send_from_directory
import os
import requests
from flask import Flask, request, jsonify, render_template, send_file
from threading import Timer
from flask_cors import CORS
import updata_data
import withdraw_data
import io
from io import BytesIO
import location

app = Flask(__name__)
CORS(app)

import json


@app.route('/')
def home():
    return render_template('index.html')


ser = ''


def save_data(loaded_dict):
    with open("data.json", "w") as file:
        json.dump(loaded_dict, file)


def read_data():
    with open("data.json", "r") as file:
        x = json.load(file)

    return x


def handle_return(loaded_dict):
    count = 0

    for key in loaded_dict['data']:
        if not loaded_dict['data'][key]['index']:
            count += 1

    index = 0
    for key in loaded_dict['data']:
        loaded_dict['data'][key]['key'] = index
        index += 1
        loaded_dict['data'][key]['bv'] = key

    # print(loaded_dict)

    return loaded_dict


def watched_ud(loaded_dict):
    count_false = sum(1 for item in loaded_dict['data'].values() if item.get('index') is False)
    print(count_false)
    loaded_dict['info']['watched'] = count_false
    loaded_dict['info']['total'] = len(loaded_dict['data'])
    loaded_dict['info']['percent'] = f"{round(count_false / len(loaded_dict['data']) * 100, 1)}%"

    return loaded_dict


def watched_dic(loaded_dict):
    count = 0
    for item in loaded_dict['data']:
        if item['index'] == False:
            count += 1


    loaded_dict['info']['watched'] = count
    loaded_dict['info']['total'] = len(loaded_dict['data'])
    loaded_dict['info']['percent'] = f"{round(count / len(loaded_dict['data']) * 100, 1)}%"

    return loaded_dict


@app.route('/Initialize', methods=['POST'])
def Initialize():
    datas = read_data()

    return jsonify(datas)


@app.route('/update_new', methods=['POST'])
def get_update():
    data = request.get_json()
    up = data.get('up')

    updata_data.updata_another(up)
    data = handle_return(read_data())

    save_data(data)
    location.save_location(data['info']['up'], data)
    return jsonify(data)


@app.route('/del', methods=['POST'])
def Del():
    data = request.get_json()
    bv = data.get('bv')
    print(bv)

    loaded_dict = read_data()

    withdraw_data.save_withdraw_data()
    index = None
    for i, item in enumerate(loaded_dict['data']):
        print(item, bv, type(item))
        if type(item) == dict:
            if item.get('bv') == bv:
                loaded_dict['data'][i]['index'] = False
                save_data(watched_dic(loaded_dict))
                return jsonify('success2')
        else:
            if item == bv:
                loaded_dict['data'][item]['index'] = False
                save_data(watched_ud(loaded_dict))
                return jsonify('success1')

    if index is not None:
        pass

    else:
        return jsonify('bv not found in dictionary')


@app.route('/updata', methods=['POST'])
def updata():
    data = request.get_json()
    up = data.get('up')
    updata_data.updata_main(up)
    return jsonify(handle_return(read_data()))


@app.route('/withdraw', methods=['POST'])
def withdraw():
    last_data = withdraw_data.withdraw_data()
    if last_data:
        save_data(last_data)
        return last_data
    else:
        return '-1'


@app.route('/backup', methods=['POST'])
def backup():
    data = read_data()
    up = data['info']['up']
    location.save_location(up, data)

    return 'success'


@app.route('/set_watched', methods=['POST'])  # 正确的拼写
def set_watched():
    data = request.get_json()
    bv = data.get('bv')
    ser = data.get('ser')
    up = data.get('up')
    # print(bv)
    try:
        with open("watched.json", "r") as file:
            # print(json.load(file))
            data = json.load(file)
    except json.decoder.JSONDecodeError:
        data = {}
    if ser not in data:
        data[ser] = []
    data[ser].append(bv)
    data[ser].append(up)
    # print(data)
    with open("watched.json", "w") as file:
        json.dump(data, file)

    return 'success'


@app.route('/get_watched', methods=['POST'])
def get_watched():
    data = request.get_json()
    ser = data.get('ser')
    try:
        with open("watched.json", "r", encoding='utf-8') as file:
            # print(json.load(file))
            data = json.load(file)
    except json.decoder.JSONDecodeError:
        return 'no success'

    try:
        info = data[f'{ser}'][0]
    except KeyError:
        data_dict = read_data()['data']
        first_key = next(iter(data_dict))
        return str(first_key)

    if info is not None:
        return str(info)


@app.route('/His', methods=['GET'])  # 正确的拼写
def His():
    return jsonify(location.get_location())


@app.route('/locations', methods=['POST'])  # 正确的拼写
def locations():
    data = request.get_json()
    articles = data['articles']
    info = data['info']
    name = data['name']
    data = {
        'data': articles,
        'info': info
    }

    up = info['up']

    location.save_location(up, data)  # 点击item以后首先保存当前item对应的up

    current_data = location.change_current(name)  # 这一步是更新 datas->data
    # 总结就是跳转之前先保存up 然后更新传来的name
    return jsonify(current_data)


@app.route('/wav', methods=['GET'])
def wavs():
    with open('收.wav', 'rb') as audio_file:
        audio_data = audio_file.read()

    stream = io.BytesIO(audio_data)

    return send_file(stream, mimetype='audio/wav')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
