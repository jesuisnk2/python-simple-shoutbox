import sqlite3
import time

# kết nối với sqlite file
conn = sqlite3.connect('python/2407me.db')
cursor = conn.cursor()

# tạo bảng `shoutbox` nếu chưa có
cursor.execute('''
CREATE TABLE IF NOT EXISTS shoutbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    msg TEXT NOT NULL,
    time INTEGER NOT NULL
)
''')

# lưu chat mới
def insert_chat(name, msg):
    cursor.execute("INSERT INTO shoutbox (name, msg, time) VALUES (?, ?, ?)", (name, msg, int(time.time())))
    conn.commit()

# xóa chat theo id
def delete_chat(id):
    cursor.execute("DELETE FROM shoutbox WHERE id=?", (id,))
    conn.commit()

# sửa chat theo id
def update_chat(id, name, msg):
    cursor.execute("UPDATE shoutbox SET name=?, msg=? WHERE id=?", (name, msg, id))
    conn.commit()

# lấy danh sách chat có offset
def get_chat(per, page):
    offset = (page - 1) * per
    cursor.execute("SELECT * FROM shoutbox ORDER BY time DESC LIMIT ? OFFSET ?", (per, offset))
    return cursor.fetchall()

# lấy toàn bộ chat
def get_all_chat():
    cursor.execute("SELECT * FROM shoutbox ORDER BY time DESC")
    return cursor.fetchall()

# đếm chat
def count_chat():
    cursor.execute("SELECT COUNT(*) FROM shoutbox")
    return cursor.fetchone()[0]