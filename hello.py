# coding:utf-8
import inspect
import win32api
import os
from PIL import ImageGrab, Image
from pynput.keyboard import Key, Listener
from pynput.mouse import Listener
from pynput import keyboard
import pythoncom
import pytesseract  # Текстовый пакет распознавания изображений
import pyperclip

# Создаем список координат
x1 = 564
x2 = 725
y1 = 762
y2 = 792

coordinate = [x1, y1, x2, y2]


def on_click(x, y, button, pressed):
    if pressed:
        print("Mouse clicked." + str(x) + "-" + str(y) + "-" + str(button))

    if pressed and x1 < x < x2 and y1 < y < y2:
        print('WINDOW')
        # Получить текущий путь к файлу
        file_ = inspect.getfile(inspect.currentframe())
        dir_path = os.path.abspath(os.path.dirname(file_))
        file_path = dir_path + '\\read.jpg'

        print(file_path)

        # Захват изображения координат
        pic = ImageGrab.grab(coordinate)
        pic.save(file_path)
        text = pytesseract.image_to_string(Image.open(file_path), lang='chi_sim')  # Определить и вернуть
        pyperclip.copy(text.replace(' ', ''))  # Импортировать содержимое распознавания в системный буфер обмена

        print(text)


def on_press(key):
    print("key is pressed")


# Слушайте события клавиатуры
def on_mouse_event(event):
    # Получить текущий путь к файлу
    file_ = inspect.getfile(inspect.currentframe())
    dir_path = os.path.abspath(os.path.dirname(file_))
    file_path = dir_path + '\\read.jpg'
    # Мониторинг событий мыши
    if event.MessageName == 'mouse left down':
        coordinate[0:2] = event.Position
    elif event.MessageName == 'mouse left up':
        coordinate[2:4] = event.Position
        win32api.PostQuitMessage()  # Выйти из цикла мониторинга
        # Захват изображения координат
        pic = ImageGrab.grab(coordinate)
        pic.save(file_path)
        text = pytesseract.image_to_string(Image.open(file_path), lang='chi_sim')  # Определить и вернуть
        pyperclip.copy(text.replace(' ', ''))  # Импортировать содержимое распознавания в системный буфер обмена
    return True


if __name__ == '__main__':
    # key_listener = keyboard.Listener(on_press=on_press)
    # key_listener.start()

    with Listener(on_click=on_click) as listener:
        listener.join()

    # hm = pyHook.HookManager()  # Создаем объект управления ловушкой
    # hm.MouseAll = on_mouse_event  # Мониторинг всех событий мыши
    # hm.HookMouse()  # Установить крючок для мыши
    # pythoncom.PumpMessages()  # Входим в цикл, программа слушала
