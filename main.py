# coding:utf-8
import inspect
import os
import time
import tkinter

import pyperclip
import pytesseract  # Текстовый пакет распознавания изображений
from PIL import ImageGrab, Image
from pynput.mouse import Listener

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "Tesseract-OCR"'

# Создаем список координат
x1 = 620
x2 = 670
y1 = 765
y2 = 793
coordinate = [x1, y1, x2, y2]


def on_click(x, y, button, pressed):
    # if pressed:
    #     print("Mouse clicked. \n x=" + str(x) + "\n y=" + str(y))

    work_zone = [342, 300, 442, 855]

    if pressed and work_zone[0] < x < work_zone[2] and work_zone[1] < y < work_zone[3]:
        # print('work_zone!')
        screenAndCalc(0.7)


def screenAndCalc(sleep_time=0.0):
    time.sleep(sleep_time)
    # Получить текущий путь к файлу
    file_ = inspect.getfile(inspect.currentframe())
    dir_path = os.path.abspath(os.path.dirname(file_))
    file_path = dir_path + '\\read.jpg'

    # Захват изображения координат
    pic = ImageGrab.grab(coordinate)
    pic.save(file_path)

    # text = pytesseract.image_to_string(Image.open(file_path), config='--psm 7')
    text = pytesseract.image_to_string(Image.open(file_path), lang='eng',
                                       config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    # pyperclip.copy(text.replace(' ', ''))  # Импортировать содержимое распознавания в системный буфер обмена
    # print(text)
    if text:
        labelRead.config(text="FOUND: " + text.strip('\n'), pady=0, bg='white')
        result50 = float(text) * 0.5
        price50btn.config(text="50% - " + str(int(result50)), command=lambda: copyBuyPrice(result50))
        result55 = float(text) * 0.55
        price55btn.config(text="55% - " + str(int(result55)), command=lambda: copyBuyPrice(result55))
        result60 = float(text) * 0.6
        price60btn.config(text="60% - " + str(int(result60)), command=lambda: copyBuyPrice(result60))
        result65 = float(text) * 0.65
        price65btn.config(text="65% - " + str(int(result65)), command=lambda: copyBuyPrice(result65))
    else:
        labelRead.config(text="NOT FOUND", pady=0, bg="red")
        price50btn.config(text="50%", command='')
        price55btn.config(text="55%", command='')
        price60btn.config(text="60%", command='')
        price65btn.config(text="65%", command='')


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

        root.geometry("75x152+705+602")

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
