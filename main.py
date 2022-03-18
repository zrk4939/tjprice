# coding:utf-8
import inspect
import os
import tkinter

import pytesseract  # Текстовый пакет распознавания изображений
from PIL import ImageGrab, Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "Tesseract-OCR"'

# Создаем список координат
x1 = 620
x2 = 670
y1 = 765
y2 = 793
coordinate = [x1, y1, x2, y2]


def screenAndCalc():
    # Получить текущий путь к файлу
    file_ = inspect.getfile(inspect.currentframe())
    dir_path = os.path.abspath(os.path.dirname(file_))
    file_path = dir_path + '\\read.jpg'

    # Захват изображения координат
    pic = ImageGrab.grab(coordinate)
    pic.save(file_path)

    # text = pytesseract.image_to_string(Image.open(file_path), config='--psm 7')
    text = pytesseract.image_to_string(Image.open(file_path), lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    # pyperclip.copy(text.replace(' ', ''))  # Импортировать содержимое распознавания в системный буфер обмена
    # print(text)
    labelRead.config(text="FOUND: " + text.strip('\n'), pady=0)
    if text:
        result50 = float(text) * 0.5
        label50.config(text="50% - " + str(int(result50)))
        result55 = float(text) * 0.55
        label55.config(text="55% - " + str(int(result55)))
        result60 = float(text) * 0.6
        label60.config(text="60% - " + str(int(result60)))


# creating the tkinter window
root = tkinter.Tk()
root.attributes("-topmost", True)

root.geometry("75x102+705+652")

labelRead = tkinter.Label(root, text='FOUND', pady=0)
label50 = tkinter.Label(root, text='50%')
label55 = tkinter.Label(root, text='55%')
label60 = tkinter.Label(root, text='60%')
labelRead.pack()
label50.pack()
label55.pack()
label60.pack()

button = tkinter.Button(root, text="Update", padx=5, pady=10)
button.config(command=screenAndCalc)
button.pack()

root.overrideredirect(1)
root.mainloop()
