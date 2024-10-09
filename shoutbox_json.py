import json
import os
import time

# tạo file json để lưu giữ liệu
json_file = "python/2407me.json"
if not os.path.exists(json_file):
    with open(json_file, 'w') as file:
        json.dump([], file)  # Lưu danh sách rỗng

# đọc dữ liệu từ file JSON
def read_json():
    with open(json_file, 'r') as file:
        return json.load(file)

# ghi dữ liệu vào file JSON
def write_json(data):
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

# lưu chat mới
def insert_chat(name, msg):
    data = read_json()
    # Lấy id mới (tăng tự động)
    new_id = max([chat['id'] for chat in data], default=0) + 1
    # Thêm bản ghi mới
    new_chat = {"id": new_id, "name": name, "msg": msg, "time": int(time.time())}
    data.append(new_chat)
    # Lưu lại vào file JSON
    write_json(data)

# xóa chat theo id
def delete_chat(id):
    data = read_json()
    # Xóa chat có id tương ứng
    data = [chat for chat in data if chat["id"] != id]
    # Lưu lại vào file JSON
    write_json(data)

# sửa chat theo id
def update_chat(id, name, msg):
    data = read_json()
    # Cập nhật chat có id tương ứng
    for chat in data:
        if chat["id"] == id:
            chat["name"] = name
            chat["msg"] = msg
            break
    
    # Lưu lại vào file JSON
    write_json(data)

# Lấy danh sách chat có offset
def get_chat(per, page):
    data = read_json()
    # Tính offset và lấy bản ghi
    offset = (page - 1) * per
    return data[offset:offset + per]

# Lấy toàn bộ chat
def get_all_chat():
    return read_json()

# Đếm số lượng chat
def count_chat():
    data = read_json()
    return len(data)