import pyautogui
import cv2
import numpy as np
import time
import win32gui
import pygetwindow as gw

# Liên quan đến tạm dừng chương trình
import keyboard


# Đường dẫn tới hình ảnh mẫu mà bạn muốn tìm
image_path = ".\\ss.png"
target_window = "By Unkoe"

# Biến để quản lý trạng thái lặp
running = False

# Đọc hình ảnh mẫu bằng OpenCV
template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
template_w, template_h = template.shape[::-1]


# Thiết lập độ nhạy (độ chính xác) khi so khớp hình ảnh
threshold = 0.9

screenshot = "unknow"
result = "unknow"
loc = "unknow"


def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        return win32gui.GetWindowText(hwnd)
    return target_window


def set_active_window(window_title):
    windowNeedActive = gw.getWindowsWithTitle(window_title)
    if len(windowNeedActive) != 0:
        windowNeedActive[0].activate()


def auto_press():
    try:
        # Chụp ảnh màn hình
        screenshot = pyautogui.screenshot()

        # Chuyển ảnh chụp màn hình thành định dạng OpenCV
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        # Tìm vị trí của hình ảnh mẫu trong ảnh chụp màn hình
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)

        hasImage = loc[::-1][0].__len__() != 0
        if hasImage:
            # Lấy cửa sổ hiện tại
            active_window_title = get_active_window_title()

            set_active_window(target_window)
            pyautogui.press("f9")
            set_active_window(active_window_title)
            time.sleep(0.1)

        # Thêm thời gian chờ để tránh sử dụng quá nhiều tài nguyên hệ thống
        time.sleep(1)
    except:
        print(
            "Hãy click vào màn hình của game để khởi động lại, nếu không được nữa thì khởi động lại game"
        )


print("Nhấn phím = để bắt đầu auto. Nhấn giữ phím = để tạm dừng auto. ")
print("Nhấn phím ALT + F3 để thoát.")

while True:
    if keyboard.is_pressed("alt+f3"):
        print("Thoát chương trình.")
        break

    if keyboard.is_pressed("="):
        running = not running
        if running:
            print("Bắt đầu auto.")
        else:
            print("Dừng auto.")
        # Đợi cho đến khi phím = được thả để tránh lặp lại việc bật/tắt
        while keyboard.is_pressed("="):
            time.sleep(0.1)

    if running:
        auto_press()
