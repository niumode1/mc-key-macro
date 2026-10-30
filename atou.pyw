import tkinter as tk
import time
import threading
import sys
from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# 键鼠控制
kb = KeyboardController()
mouse = MouseController()

# 两个模式完全独立，互斥运行
macro_running = False    # 万箭模式状态
left_running = False     # 左键模式状态
stop_flag = False

# 纯左键连击 + 强制常驻按住空格（修复手动按空格冲突bug）
def left_click_loop():
    global left_running, stop_flag
    left_running = True
    # 先按下空格
    kb.press(Key.space)
    try:
        while not stop_flag:
            # 每次循环都强制保持空格按下，覆盖手动操作
            kb.press(Key.space)
            mouse.click(Button.left)
            time.sleep(0.2)
    finally:
        # 彻底停止再松开空格
        kb.release(Key.space)
        left_running = False

# 原宏任务（万箭模式）
def macro_loop():
    global macro_running, stop_flag
    macro_running = True
    while not stop_flag:
        # 2 按下抬起
        kb.press('2')
        time.sleep(0.05)
        kb.release('2')
        time.sleep(0.05)

        # 右键长按700ms
        mouse.press(Button.right)
        time.sleep(0.7)
        mouse.release(Button.right)
        time.sleep(0.1)

        # 1 按下抬起
        kb.press('1')
        time.sleep(0.05)
        kb.release('1')
        time.sleep(0.05)

        # 左键6次
        for _ in range(6):
            mouse.click(Button.left)
            time.sleep(0.2)
    macro_running = False

# F9 单独控制：万箭模式
def toggle_macro():
    global stop_flag, macro_running
    # 如果左键正在运行，F9 无效
    if left_running:
        return
    
    if not macro_running:
        # 启动万箭
        stop_flag = False
        lbl_status.config(text="🟢 万箭运行中", fg="green")
        threading.Thread(target=macro_loop, daemon=True).start()
    else:
        # 停止万箭
        stop_flag = True
        macro_running = False
        lbl_status.config(text="🔴 已停止", fg="red")

# F12 单独控制：纯左键+常驻空格
def toggle_left():
    global stop_flag, left_running
    # 如果万箭正在运行，F12 无效
    if macro_running:
        return
    
    if not left_running:
        # 启动左键
        stop_flag = False
        lbl_status.config(text="🟢 左键运行中", fg="blue")
        threading.Thread(target=left_click_loop, daemon=True).start()
    else:
        # 停止左键
        stop_flag = True
        left_running = False
        lbl_status.config(text="🔴 已停止", fg="red")

# 退出程序（彻底修复：停止所有 + 松按键 + 杀线程）
def exit_program():
    global stop_flag, macro_running, left_running
    # 1. 立即停止所有循环
    stop_flag = True
    # 2. 重置所有运行状态
    macro_running = False
    left_running = False
    # 3. 强制松开所有可能卡住的键
    kb.release(Key.space)
    kb.release('1')
    kb.release('2')
    mouse.release(Button.left)
    mouse.release(Button.right)
    # 4. 销毁窗口并退出
    root.destroy()
    sys.exit(0)

# 界面
root = tk.Tk()
root.title("")
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.9)
root.geometry("100x25+0+0")

lbl_status = tk.Label(root, text="🔴 已停止", fg="red", font=("Microsoft YaHei", 7))
lbl_status.pack(expand=True, fill=tk.BOTH)

# ------------------------------
# 快捷键
# F9  = 万箭模式 启停
# F12 = 左键+空格常驻 启停
# F10 = 退出
# ------------------------------
pressed_keys = set()

def on_press_record(key):
    pressed_keys.add(key)

def on_release_record(key):
    if key in pressed_keys:
        pressed_keys.discard(key)

listener = keyboard.Listener(on_press=on_press_record, on_release=on_release_record)
listener.daemon = True
listener.start()

# F9 万箭启停
def check_f9():
    try:
        if Key.f9 in pressed_keys:
            toggle_macro()
            while Key.f9 in pressed_keys:
                time.sleep(0.1)
    finally:
        root.after(50, check_f9)

# F10 退出
def check_f10():
    try:
        if Key.f10 in pressed_keys:
            exit_program()
    finally:
        root.after(50, check_f10)

# F12 左键启停
def check_f12():
    try:
        if Key.f12 in pressed_keys:
            toggle_left()
            while Key.f12 in pressed_keys:
                time.sleep(0.1)
    finally:
        root.after(50, check_f12)

root.after(50, check_f9)
root.after(50, check_f10)
root.after(50, check_f12)
root.mainloop()