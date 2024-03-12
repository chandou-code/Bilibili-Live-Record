# # -*- coding: utf-8 -*-
import json
import app

def withdraw_data():
    try:
        with open("withdraw.json", "r") as file:
            datas = json.load(file)
    except json.decoder.JSONDecodeError:
        datas = {}
    if datas:
        last_key = str(len(datas))  # 获取最后一个数据的键值
        last_data = datas[last_key]  # 获取最后一个数据

        del datas[last_key]  # 删除最后一个数据

        with open("withdraw.json", "w") as file:
            json.dump(datas, file)

        return last_data
    else:
        return False




def save_withdraw_data():
    try:
        with open("withdraw.json", "r") as file:
            datas = json.load(file)
    except json.decoder.JSONDecodeError:
        datas = {}
    times = 5
    if not datas:
        with open("data.json", "r") as file:
            loaded_data = json.load(file)
        datas = {1: loaded_data}
    elif len(datas) < times:
        with open("data.json", "r") as file:
            loaded_data = json.load(file)
        next_key = len(datas) + 1
        datas[next_key] = loaded_data
    else:
        with open("data.json", "r") as file:
            loaded_data = json.load(file)
        for i in range(1, times):
            datas[str(i)] = datas[str(i + 1)]
        datas[str(times)] = loaded_data

    with open("withdraw.json", "w") as file:
        json.dump(datas, file)



# withdraw_data()
# save_withdraw_data()
