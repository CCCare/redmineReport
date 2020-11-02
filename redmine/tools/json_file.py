import json

def write_json_file(dict_obj,file_path):
    # dict_obj = json.loads(json_str)
    with open(file_path, "w") as f:
        json.dump(dict_obj, f)
    print("加载入文件完成...")

def read_json_file(file_path):
    a={}
    with open(file_path, 'r') as f:
        if f is not None:
            a = json.load(f)  # 此时a是一个字典对象
    return a

if __name__ == '__main__':
    a = read_json_file("../alarm/alarm_bug.json")
    print(a)