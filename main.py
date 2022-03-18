# coding:utf-8
import inspect
import os
import tkinter
import pytesseract  # Текстовый пакет распознавания изображений
from PIL import ImageGrab, Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Создаем список координат
x1 = 564
x2 = 725
y1 = 762
y2 = 792
coordinate = [x1, y1, x2, y2]


def on_click(x, y, button, pressed):
    if pressed:
        print("Mouse clicked. \n x=" + str(x) + "\n y=" + str(y))

    if pressed and x1 < x < x2 and y1 < y < y2:
        screenAndCalc()


def screenAndCalc():
    # Получить текущий путь к файлу
    file_ = inspect.getfile(inspect.currentframe())
    dir_path = os.path.abspath(os.path.dirname(file_))
    file_path = dir_path + '\\read.jpg'

    # Захват изображения координат
    pic = ImageGrab.grab(coordinate)
    pic.save(file_path)
    text = pytesseract.image_to_string(Image.open(file_path))  # Определить и вернуть
    # pyperclip.copy(text.replace(' ', ''))  # Импортировать содержимое распознавания в системный буфер обмена
    # print(text)
    if text:
        result50 = float(text) * 0.5
        label50.config(text="50% - " + str(int(result50)))
        result55 = float(text) * 0.55
        label55.config(text="55% - " + str(int(result55)))
        result60 = float(text) * 0.6
        label60.config(text="60% - " + str(int(result60)))


# creating the tkinter window
root = tkinter.Tk()
# Main_window.attributes('-alpha', 0.3)
# root.overrideredirect(True)
root.attributes("-topmost", True)
# root.wm_attributes("-transparent", True)
# root.config(bg='')

root.geometry("75x92+705+662")

label50 = tkinter.Label(root, text='50%')
label55 = tkinter.Label(root, text='55%')
label60 = tkinter.Label(root, text='60%')
label50.pack()
label55.pack()
label60.pack()

button = tkinter.Button(root, text="Update", padx=5, pady=10)
button.config(command=screenAndCalc)
button.pack()

root.overrideredirect(1)
root.mainloop()
