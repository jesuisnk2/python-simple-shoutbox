import time
from datetime import datetime

# thời gian đăng
def ago(time_ago):
    time_ago = int(time_ago)
    current_time = int(time.time())  # Thời gian hiện tại (epoch time)
    elapsed_seconds = current_time - time_ago  # Số giây đã trôi qua
    elapsed_minutes = elapsed_seconds // 60  # Số phút đã trôi qua
    elapsed_days = (datetime.fromtimestamp(current_time).timetuple().tm_yday - 
                    datetime.fromtimestamp(time_ago).timetuple().tm_yday)  # Số ngày đã trôi qua
    full_time = datetime.fromtimestamp(time_ago).strftime('%d.%m.%Y - %H:%M')  # Định dạng thời gian đầy đủ
    short_time = datetime.fromtimestamp(time_ago).strftime('%H:%M')  # Định dạng thời gian ngắn
    if elapsed_days == 0:
        if elapsed_seconds <= 60:
            return f'{elapsed_seconds} giây trước'
        elif elapsed_minutes < 60:
            return f'{elapsed_minutes} phút trước'
        else:
            return f'Hôm nay, {short_time}'
    elif elapsed_days == 1:
        return f'Hôm qua, {short_time}'
    else:
        return full_time