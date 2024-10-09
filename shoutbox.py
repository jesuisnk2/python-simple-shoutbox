#import shoutbox_sqlite as shoutbox
import k_func as k_func

# SHOUTBOX
print('Simple Shoutbox')
# chon kiểu csdl
db_type = 'json' # sqlite, csv, json
match db_type:
    case 'sqlite':
        import shoutbox_sqlite as shoutbox
    case 'csv':
        import shoutbox_csv as shoutbox
    case 'json':
        import shoutbox_json as shoutbox

# lặp lại vô hạn sau kết thúc các lệnh
while True:
    print('--- DANH SÁCH ---')
    # lấy danh sách chat
    if shoutbox.count_chat() > 0: 
        for chat in shoutbox.get_all_chat():
            # kiểm tra kiểu csdl
            if db_type == 'sqlite':
                id, name, msg, time = int(chat[0]), str(chat[1]), str(chat[2]), int(chat[3])
            else: # csv, json
                id, name, msg, time = chat["id"], chat["name"], chat["msg"], chat["time"]
            print(f'{id}) <{name}>: {msg} ({k_func.ago(time)})\n')
    else:
        print('Chưa có tin nhắn nào.')

    print('--- CHAT ---')
    # Nhập nội dung
    name, msg = input('Tên của bạn: '), input('Nội dung: ')
    # Duyệt sau khi đã nhập nội dung
    while len(name) < 3 or len(msg) < 5:
        print('Tên và nội dung phải dài hơn 3 ký tự và 5 ký tự.')
        # Nhập lại
        name, msg = input('Tên của bạn: '), input('Nội dung: ')

    # Ghi dữ liệu vào cơ sở dữ liệu
    shoutbox.insert_chat(name, msg)
