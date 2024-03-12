import json
import os
import withdraw_data
import updata_data


def get_file_names_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("指定路径不是一个文件夹")
        return

    file_names = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]

    return file_names


def get_location():
    file_names = get_file_names_in_folder("./datas")
    ups = []
    if file_names is not None:
        # print(f"文件夹 '{folder_path}' 下的文件数量为: {len(file_names)}")
        for name in file_names:
            s = name.split('_')[-2]
            ups.append(s)

        return ups


def save_location(name, loaded_dict):
    with open(f"./datas/{name}_data.json", "w") as file:
        json.dump(loaded_dict, file)


def detail_location(name):
    try:
        with open(f"./datas/{name}_data.json", "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return False


def change_current(name):
    # 根据name获得datas内的json 如果没有那就根据name更新 更新完以后就写入到当前data.json内
    current_data = detail_location(name)
    if not current_data:
        withdraw_data.save_withdraw_data()
        current_data = updata_data.updata_another(name)

    with open("data.json", "w") as file:
        json.dump(current_data, file)

    return current_data


if __name__ == '__main__':
    # print()
    get_location()
