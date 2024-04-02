# # -*- coding: utf-8 -*-
import json
from bs4 import BeautifulSoup
import requests


def get_all_pn(pn, mid, series_id):
    # mid = "672328094"
    # series_id = "222940"
    # url = f'https://api.bilibili.com/x/series/archives?mid=11073&series_id=407852&only_normal=true&sort=desc&pn={pn}&ps=30&current_mid=12310947'
    url = f'https://api.bilibili.com/x/series/archives?mid={mid}&series_id={series_id}&only_normal=true&sort=desc&pn={pn}&ps=30&current_mid=12310947'
    headers = {
        'Cookie':此处填自己的Cookie ,
    
        'User-Agent': r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"

    }
    r = requests.get(url, headers=headers)
    # print(r.text)
    # print(r.status_code)
    datae = r.text
    # print(datae)
    data = json.loads(datae)
    all_pn = data['data']['archives']
    return all_pn


def get_name_mid(keyword):

    url = f'https://search.bilibili.com/upuser?keyword={keyword}&from_source=webtop_search&spm_id_from=333.1007&search_source=5'
    headers = {
        'Cookie': 此处填自己的Cookie,
        'User-Agent': r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"

    }
    r = requests.get(url, headers=headers)

    datae = r.text

    soup = BeautifulSoup(datae, 'html.parser')

    h2_tag = soup.select_one('h2.b_text.i_card_title.mt_0')
    text_content = h2_tag.get_text()
    href = h2_tag.find('a').get('href')
    return href, text_content


def get_ser(up):
    # print('up',up)
    href, text_content = get_name_mid(up)
    # print( href, text_content)
    uid = href.split('/')[-1]

    # print(uid)
    url = f'https://api.bilibili.com/x/polymer/web-space/seasons_series_list?mid={uid}&page_num=1&page_size=20&web_location=333.999&w_rid=ac2956f6caa2c1752a95cc390e9e7b8c&wts=1709695118'
    headers = {
        'Cookie':此处填自己的Cookie,
        'User-Agent': r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"

    }
    r = requests.get(url, headers=headers)

    datae = r.text

    data = json.loads(datae)

    i = 0
    while True:
        name = data['data']['items_lists']['series_list'][i]['meta']['name']

        if name == '直播回放':
            ser = data['data']['items_lists']['series_list'][i]['meta']['series_id']
            return ser, uid, text_content

        i += 1




def get_bv_name(all_pn):
    BV = all_pn['bvid']
    Name = all_pn['title']
    return BV, Name


def updata_hanser(NAme):

    new_dict = {}
    ser, uid, text_content = get_ser(f'{NAme}')
    print(ser, uid, text_content)
    i = 1
    while True:
        all_pn = get_all_pn(i, uid, ser)
        i += 1
        if not all_pn:
            break

        for pn in all_pn:
            BV, Name = get_bv_name(pn)
            new_dict[BV] = {
                "title": Name,
                "index": True
            }

    new_dict['up'] = text_content
    new_dict['ser'] = ser
    new_dict['uid'] = uid
    print(new_dict)
    return new_dict


def updata_main(NAme):
    with open("data.json", "r") as file:
        loaded_dict = json.load(file)
    loaded_dict = loaded_dict['data']
    new_dict = updata_hanser(NAme)

    up = new_dict.get('up', {})  # 获取'up'键对应的值，如果键不存在，默认为一个空字典
    ser = new_dict.get('ser', {})  # 获取'ser'键对应的值，如果键不存在，默认为一个空字典
    uid = new_dict.get('uid', {})  # 获取'uid'键对应的值，如果键不存在，默认为一个空字典

    del new_dict['up']
    del new_dict['uid']
    del new_dict['ser']

    set1 = set(new_dict) - set(loaded_dict)

    dic = {s: new_dict[s] for s in set1}
    dic.update(loaded_dict)

    dic2 = dic.copy()
    dic.clear()
    dic['data'] = {}
    dic['data'] = dic2  # 将dic内的所有内容复制到data字段下

    dic['info'] = {}
    # 将'up'、'ser'、'uid'键对应的值更新到最终字典中
    dic['info']['up'] = up
    dic['info']['ser'] = ser
    dic['info']['uid'] = uid

    with open("data.json", "w") as file:
        json.dump(dic, file)

    return dic


def handle_data(new_dict):
    up = new_dict.get('up', {})  # 获取'up'键对应的值，如果键不存在，默认为一个空字典
    ser = new_dict.get('ser', {})  # 获取'ser'键对应的值，如果键不存在，默认为一个空字典
    uid = new_dict.get('uid', {})  # 获取'uid'键对应的值，如果键不存在，默认为一个空字典

    del new_dict['up']
    del new_dict['uid']
    del new_dict['ser']
    dic2 = new_dict.copy()
    new_dict.clear()
    new_dict['data'] = {}
    new_dict['data'] = dic2  # 将dic内的所有内容复制到data字段下

    new_dict['info'] = {}
    # 将'up'、'ser'、'uid'键对应的值更新到最终字典中
    new_dict['info']['up'] = up
    new_dict['info']['ser'] = ser
    new_dict['info']['uid'] = uid
    return new_dict


def updata_another(NAme):
    new_dict = updata_hanser(NAme)
    new_dict = handle_data(new_dict)
    with open("data.json", "w") as file:
        json.dump(new_dict, file)
    return new_dict

# if __name__ == '__main__':
#     # print(updata_main())
#     updata_main('嘉然')
