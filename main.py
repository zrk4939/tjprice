# coding:utf-8
import inspect
import os
import time
import tkinter
from threading import Timer

import pyperclip
import pytesseract  # Текстовый пакет распознавания изображений
from PIL import ImageGrab, ImageEnhance
from pynput.mouse import Listener

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "Tesseract-OCR"'


def on_click(x, y, button, pressed):
    # if pressed:
    #     print("Mouse clicked. \n x=" + str(x) + "\n y=" + str(y))

    # Создаем список координат (исходник 1920x1080)
    wz_tl = res_conv(342, 300, (1920, 1080), active_resolution)  # work_zone top-left
    wz_rb = res_conv(442, 855, (1920, 1080), active_resolution)  # work_zone right-bottom
    work_zone = [wz_tl[0], wz_tl[1], wz_rb[0], wz_rb[1]]  # [x1, y1, x2, y2]

    if pressed and work_zone[0] < x < work_zone[2] and work_zone[1] < y < work_zone[3]:
        # print('work_zone!')
        t = Timer(0.2, screenAndCalc)
        t.start()


def screenAndCalc(sleep_time=0.0):
    time.sleep(sleep_time)

    modifier = 10

    # Создаем список координат (исходник 1920x1080)
    coordinate_tl = res_conv(620, 765, (1920, 1080), active_resolution)  # coordinate top-left
    coordinate_rb = res_conv(670, 790, (1920, 1080), active_resolution)  # coordinate right-bottom
    coordinates = [coordinate_tl[0], coordinate_tl[1], coordinate_rb[0], coordinate_rb[1]]  # [x1, y1, x2, y2]

    # Захват изображения координат
    pic = ImageGrab.grab(coordinates)
    pic = pic.resize((pic.size[0] * modifier, pic.size[1] * modifier))
    # pic = pic.convert("L") # convert image to black and white
    bwFilter = ImageEnhance.Color(pic)
    pic = bwFilter.enhance(0)
    contrastFilter = ImageEnhance.Contrast(pic)
    pic = contrastFilter.enhance(3)
    sharpnessFilter = ImageEnhance.Sharpness(pic)
    pic = sharpnessFilter.enhance(50)

    # Получить текущий путь к файлу
    # file_ = inspect.getfile(inspect.currentframe())
    # dir_path = os.path.abspath(os.path.dirname(file_))
    # file_path = dir_path + '\\read.jpg'
    # pic.save(file_path)

    text = recognize(pic)
    # pyperclip.copy(text.replace(' ', ''))  # Импортировать содержимое распознавания в системный буфер обмена
    # print(text)
    if text:
        labelRead.config(text="FOUND: " + text.strip('\n'), pady=0, bg='white')
        result50 = float(text) * 0.5
        result55 = float(text) * 0.55
        result60 = float(text) * 0.6
        result65 = float(text) * 0.65

        copyBuyPrice(result65)  # СРАЗУ помещаем в буфер 65%

        price50btn.config(text="50% - " + str(int(result50)), command=lambda: copyBuyPrice(result50))
        price55btn.config(text="55% - " + str(int(result55)), command=lambda: copyBuyPrice(result55))
        price60btn.config(text="60% - " + str(int(result60)), command=lambda: copyBuyPrice(result60))
        price65btn.config(text="65% - " + str(int(result65)), command=lambda: copyBuyPrice(result65))
    else:
        labelRead.config(text="NOT FOUND", pady=0, bg="red")
        price50btn.config(text="50%", command='')
        price55btn.config(text="55%", command='')
        price60btn.config(text="60%", command='')
        price65btn.config(text="65%", command='')

        pyperclip.copy('')  # очистить буфер


def recognize(pic):
    try:
        value = pytesseract.image_to_string(pic, lang='eng',
                                            config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        if not value or (int(value) <= 10):
            value = pytesseract.image_to_string(pic, config='--psm 11 digits')

        if int(value) > 10:
            return value
        else:
            return ''
    except:
        return ''


def res_conv(x: int, y: int, resolution_from: tuple, resolution_to: tuple) -> tuple:
    assert x < resolution_from[0] and y < resolution_from[1], "Input coordinate is larger than resolution"
    x_ratio = resolution_to[0] / resolution_from[0]  # ratio to multiply x co-ord
    y_ratio = resolution_to[1] / resolution_from[1]  # ratio to multiply y co-ord
    return int(x * x_ratio), int(y * y_ratio)


def copyBuyPrice(value):
    # print(int(value))
    pyperclip.copy(int(value))  # Импортировать содержимое распознавания в системный буфер обмена


if __name__ == '__main__':
    # key_listener = keyboard.Listener(on_press=on_press)
    # key_listener.start()

    with Listener(on_click=on_click) as listener:
        # creating the tkinter window
        root = tkinter.Tk()
        root.attributes("-topmost", True)

        # active_resolution = (GetSystemMetrics(0), GetSystemMetrics(1))
        active_resolution = (root.winfo_screenwidth(), root.winfo_screenheight())

        # Создаем список координат (исходник 1920x1080)
        geometry_tl = res_conv(705, 602, (1920, 1080), active_resolution)  # top-left
        # root.geometry("75x152+705+602")
        root.geometry("75x152+" + str(geometry_tl[0]) + "+" + str(geometry_tl[1]))

        labelRead = tkinter.Label(root, text='FOUND', pady=0, bg='white')
        price50btn = tkinter.Button(root, text='50%')
        # price50btn.config(command=copyBuyValue)
        price55btn = tkinter.Button(root, text='55%')
        # price55btn.config(command=copyBuyValue)
        price60btn = tkinter.Button(root, text='60%')
        # price60btn.config(command=copyBuyValue)
        price65btn = tkinter.Button(root, text='65%')
        # price65btn.config(command=copyBuyValue)
        # price70btn = tkinter.Button(root, text='70%')
        # price70btn.config(command=screenAndCalc)
        labelRead.pack()
        price50btn.pack()
        price55btn.pack()
        price60btn.pack()
        price65btn.pack()
        # price70btn.pack()

        button = tkinter.Button(root, text="Update", padx=5, pady=10)
        button.config(command=screenAndCalc)
        button.pack()

        root.overrideredirect(1)
        root.mainloop()

        listener.join()
