import tkinter as tk
from tkinter import messagebox, simpledialog, Frame, Scrollbar

import k_func
import bot

app_title = 'Simple Shoutbox'
time_reload = 5000  # autoload mỗi 5s

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

        # Tạo Text widget hiển thị danh sách chat
        self.chat_text = tk.Text(self.chat_frame, width=50, height=15, wrap=tk.WORD)
        self.chat_text.pack(side=tk.LEFT)

        # Tạo Scrollbar cho Text widget
        self.scrollbar = Scrollbar(self.chat_frame, command=self.chat_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_text.config(yscrollcommand=self.scrollbar.set)

        # Tạo label và entry cho tên
        self.label_name = tk.Label(master, text="Tên của bạn:")
        self.label_name.pack()
        self.entry_name = tk.Entry(master)
        self.entry_name.pack(padx=10, pady=5)

        # Tạo label và entry cho nội dung
        self.label_msg = tk.Label(master, text="Nội dung:")
        self.label_msg.pack()
        self.textarea_msg = tk.Text(master, height=10, width=40, wrap=tk.WORD)  # Sử dụng wrap=tk.WORD
        self.textarea_msg.pack(padx=10, pady=5)

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
        self.chat_text.delete(1.0, tk.END)

        # Lấy danh sách chat
        if shoutbox.count_chat() > 0:
            for chat in shoutbox.get_all_chat():
                # Kiểm tra kiểu CSDL
                if db_type == 'sqlite':
                    id, name, msg, time = int(chat[0]), str(chat[1]), str(chat[2]), int(chat[3])
                else:  # csv, json
                    id, name, msg, time = chat["id"], chat["name"], chat["msg"], chat["time"]

                # Hiển thị chat với khoảng cách giữa các từ và tự động xuống dòng
                formatted_msg = f'{id}) <{name}>: {msg} ({k_func.ago(time)})\n'
                self.chat_text.insert(tk.END, formatted_msg)
                self.chat_text.see(tk.END)
        else:
            self.chat_text.insert(tk.END, 'Chưa có tin nhắn nào.\n')

        self.master.after(time_reload, self.update_chat_display)

    def send_message(self):
        name = self.entry_name.get()
        msg = self.textarea_msg.get("1.0", tk.END).strip()  # Sử dụng textarea_msg

        # Kiểm tra điều kiện nhập
        if len(name) < 3 or len(msg) < 5:
            messagebox.showerror("Lỗi", "Tên và nội dung phải dài hơn 3 ký tự và 5 ký tự.")
            return

        # Ghi dữ liệu vào cơ sở dữ liệu
        shoutbox.insert_chat(name, msg)
        # bot trả lời
        if bot.xemboi_cmd in msg:
            shoutbox.insert_chat(bot.bot_name, bot.xemboi_get)
        # Xóa nội dung tin nhắn đã nhập, nhưng giữ lại tên
        self.textarea_msg.delete("1.0", tk.END)

    def edit_message(self):
        selected = self.chat_text.tag_ranges("sel")
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tin nhắn để sửa.")
            return

        start, end = selected
        chat_data = self.chat_text.get(start, end)
        id = int(chat_data.split(')')[0])  # Lấy ID từ chuỗi

        new_name = simpledialog.askstring("Sửa tên", "Nhập tên mới:", initialvalue=chat_data.split('<')[1].split('>')[0])
        new_msg = simpledialog.askstring("Sửa nội dung", "Nhập nội dung mới:", initialvalue=chat_data.split(': ')[1].split(' (')[0])

        if new_name and new_msg:
            shoutbox.update_chat(id, new_name, new_msg)  # Sử dụng hàm update_chat
            messagebox.showinfo("Thông báo", "Tin nhắn đã được sửa.")
            self.update_chat_display()  # Cập nhật lại danh sách chat

    def delete_message(self):
        selected = self.chat_text.tag_ranges("sel")
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tin nhắn để xóa.")
            return

        start, end = selected
        chat_data = self.chat_text.get(start, end)
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