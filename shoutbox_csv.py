import pandas as pd
import os
import time

# tạo file csv để lưu giữ liệu
csv_file = 'python/2407me.csv'
if not os.path.exists(csv_file):
    # tạo DataFrame với các cột id, name, msg, time
    df = pd.DataFrame(columns=["id", "name", "msg", "time"])
    # lưu DataFrame vào file CSV
    df.to_csv(csv_file, index=False)

# lưu chat mới
def insert_chat(name, msg):
    df = pd.read_csv(csv_file)
    # Lấy id mới (tăng tự động)
    new_id = df["id"].max() + 1 if not df.empty else 1
    # Thêm bản ghi mới vào DataFrame
    new_row = pd.DataFrame({"id": [new_id], "name": [name], "msg": [msg], "time": [int(time.time())]})
    # Sử dụng pd.concat để thêm hàng mới vào DataFrame hiện có
    df = pd.concat([df, new_row], ignore_index=True)
    # Lưu lại vào file CSV
    df.to_csv(csv_file, index=False)

# xóa chat theo id
def delete_chat(id):
    df = pd.read_csv(csv_file)
    # Xóa hàng có id tương ứng
    df = df[df["id"] != id]
    # Lưu lại vào file CSV
    df.to_csv(csv_file, index=False)

# sửa chat theo id
def update_chat(id, name, msg):
    df = pd.read_csv(csv_file)
    # Cập nhật hàng có id tương ứng
    df.loc[df["id"] == id, ["name", "msg"]] = [name, msg]
    # Lưu lại vào file CSV
    df.to_csv(csv_file, index=False)

# lấy danh sách chat có offset
def get_chat(per, page):
    df = pd.read_csv(csv_file)
    # Tính offset và lấy bản ghi
    offset = (page - 1) * per
    return df.iloc[offset:offset + per].to_dict(orient="records")

# lấy toàn bộ chat
def get_all_chat():
    df = pd.read_csv(csv_file)
    return df.to_dict(orient="records")

# đếm chat
def count_chat():
    df = pd.read_csv(csv_file)
    return len(df)