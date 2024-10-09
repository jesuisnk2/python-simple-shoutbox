import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, Frame
import time
import k_func as k_func

app_title = 'Simple Shoutbox'
time_reload = 5000 #autoload mỗi 5s

# Hàm để chọn kiểu cơ sở dữ liệu
def choose_db_type():
    db_type = simpledialog.askstring(app_title, "Nhập kiểu cơ sở dữ liệu (sqlite, csv, json):").strip().lower()
    while db_type not in ['sqlite', 'csv', 'json']:
        messagebox.showerror("Lỗi", "Kiểu cơ sở dữ liệu không hợp lệ! Vui lòng nhập lại (sqlite, csv, json).")
        db_type = simpledialog.askstring("Chọn kiểu cơ sở dữ liệu", "Nhập kiểu cơ sở dữ liệu (sqlite, csv, json):").strip().lower()
    return db_type

# Chọn kiểu CSDL
db_type = choose_db_type()
match db_type:
    case 'sqlite':
        import shoutbox_sqlite as shoutbox
    case 'csv':
        import shoutbox_csv as shoutbox
    case 'json':
        import shoutbox_json as shoutbox

class ShoutboxApp:
    def __init__(self, master):
        self.master = master
        master.title(app_title)

        # Tạo Frame để chứa danh sách chat và các nút
        self.chat_frame = Frame(master)
        self.chat_frame.pack(padx=10, pady=10)

        # Tạo Listbox hiển thị danh sách chat
        self.chat_listbox = tk.Listbox(self.chat_frame, width=50, height=15)
        self.chat_listbox.pack(side=tk.LEFT)

        # Tạo Scrollbar cho Listbox
        self.scrollbar = tk.Scrollbar(self.chat_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.chat_listbox.yview)

        # Tạo label và entry cho tên
        self.label_name = tk.Label(master, text="Tên của bạn:")
        self.label_name.pack()
        self.entry_name = tk.Entry(master)
        self.entry_name.pack(padx=10, pady=5)

        # Tạo label và entry cho nội dung
        self.label_msg = tk.Label(master, text="Nội dung:")
        self.label_msg.pack()
        self.entry_msg = tk.Entry(master)
        self.entry_msg.pack(padx=10, pady=5)

        # Tạo nút gửi
        self.send_button = tk.Button(master, text="Gửi", command=self.send_message)
        self.send_button.pack(pady=10)

        # Tạo nút sửa và xóa
        self.edit_button = tk.Button(master, text="Sửa", command=self.edit_message)
        self.edit_button.pack(side=tk.LEFT, padx=(10, 5))

        self.delete_button = tk.Button(master, text="Xóa", command=self.delete_message)
        self.delete_button.pack(side=tk.LEFT, padx=(5, 10))

        # Khởi động cập nhật chat
        self.update_chat_display()

    def update_chat_display(self):
        # Xóa nội dung hiện tại
        self.chat_listbox.delete(0, tk.END)

        # Lấy danh sách chat
        if shoutbox.count_chat() > 0:
            for chat in shoutbox.get_all_chat():
                # Kiểm tra kiểu CSDL
                if db_type == 'sqlite':
                    id, name, msg, time = int(chat[0]), str(chat[1]), str(chat[2]), int(chat[3])
                else:  # csv, json
                    id, name, msg, time = chat["id"], chat["name"], chat["msg"], chat["time"]

                # Hiển thị chat
                self.chat_listbox.insert(tk.END, f'{id}) <{name}>: {msg} ({k_func.ago(time)})')

        else:
            self.chat_listbox.insert(tk.END, 'Chưa có tin nhắn nào.')

        self.master.after(time_reload, self.update_chat_display)

    def send_message(self):
        name = self.entry_name.get()
        msg = self.entry_msg.get()

        # Kiểm tra điều kiện nhập
        if len(name) < 3 or len(msg) < 5:
            messagebox.showerror("Lỗi", "Tên và nội dung phải dài hơn 3 ký tự và 5 ký tự.")
            return

        # Ghi dữ liệu vào cơ sở dữ liệu
        shoutbox.insert_chat(name, msg)

        # Xóa nội dung tin nhắn đã nhập, nhưng giữ lại tên
        self.entry_msg.delete(0, tk.END)

    def edit_message(self):
        selected = self.chat_listbox.curselection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tin nhắn để sửa.")
            return

        index = selected[0]
        chat_data = self.chat_listbox.get(index)
        id = int(chat_data.split(')')[0])  # Lấy ID từ chuỗi

        new_name = simpledialog.askstring("Sửa tên", "Nhập tên mới:", initialvalue=chat_data.split('<')[1].split('>')[0])
        new_msg = simpledialog.askstring("Sửa nội dung", "Nhập nội dung mới:", initialvalue=chat_data.split(': ')[1].split(' (')[0])

        if new_name and new_msg:
            shoutbox.update_chat(id, new_name, new_msg)  # Sử dụng hàm update_chat
            messagebox.showinfo("Thông báo", "Tin nhắn đã được sửa.")
            self.update_chat_display()  # Cập nhật lại danh sách chat

    def delete_message(self):
        selected = self.chat_listbox.curselection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tin nhắn để xóa.")
            return

        index = selected[0]
        chat_data = self.chat_listbox.get(index)
        id = int(chat_data.split(')')[0])  # Lấy ID từ chuỗi

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tin nhắn này?")
        if confirm:
            shoutbox.delete_chat(id)  # Sử dụng hàm delete_chat
            messagebox.showinfo("Thông báo", "Tin nhắn đã được xóa.")
            self.update_chat_display()  # Cập nhật lại danh sách chat

# Tạo ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = ShoutboxApp(root)
    root.mainloop()