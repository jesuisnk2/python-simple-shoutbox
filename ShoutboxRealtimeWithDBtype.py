import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import k_func as k_func

app_title = 'Simple chatbox'

# Hàm để chọn kiểu cơ sở dữ liệu
def choose_db_type():
    db_type = simpledialog.askstring(app_title, "Nhập kiểu cơ sở dữ liệu (sqlite, csv, json):").strip().lower()
    while db_type not in ['sqlite', 'csv', 'json']:
        messagebox.showerror("Lỗi", "Kiểu cơ sở dữ liệu không hợp lệ! Vui lòng nhập lại (sqlite, csv, json).")
        db_type = simpledialog.askstring(app_title, "Nhập kiểu cơ sở dữ liệu (sqlite, csv, json):").strip().lower()
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

        # Tạo widget hiển thị danh sách chat
        self.chat_display = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
        self.chat_display.pack(padx=10, pady=10)

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

        # Khởi động cập nhật chat
        self.update_chat_display()

    def update_chat_display(self):
        # Xóa nội dung hiện tại
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)

        # Lấy danh sách chat
        if shoutbox.count_chat() > 0:
            for chat in shoutbox.get_all_chat():
                # Kiểm tra kiểu CSDL
                if db_type == 'sqlite':
                    id, name, msg, time = int(chat[0]), str(chat[1]), str(chat[2]), int(chat[3])
                else:  # csv, json
                    id, name, msg, time = chat["id"], chat["name"], chat["msg"], chat["time"]

                # Hiển thị chat
                self.chat_display.insert(tk.END, f'{id}) <{name}>: {msg} ({k_func.ago(time)})\n')
        else:
            self.chat_display.insert(tk.END, 'Chưa có tin nhắn nào.\n')

        self.chat_display.config(state='disabled')
        self.master.after(5000, self.update_chat_display)  # Cập nhật mỗi 5 giây

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

# Tạo ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = ShoutboxApp(root)
    root.mainloop()