from tkinter import *
from tkinter import ttk
import re
from tkinter.messagebox import showinfo
import controller


def truncate_error():
    showinfo(title="Ошибка", message="Не удалось очистить таблицу абонентов")


def truncate_pass():
    showinfo(title="Информация", message="Таблица абонентов была очищена")


def add_error_massage():
    showinfo(title="Ошибка", message="Вводите по шаблону:\nФамилия Имя Отчество [+7|8]xxxxxxxxxx")


def add_error_massage_2():
    showinfo(title="Ошибка", message="Номер телефона уже есть в базе")


def add_pass_massage(user):
    showinfo(title="Информация", message=f"Абонент {user} успешно добавлен")


def dell_pass_massage(user):
    showinfo(title="Информация", message=f"Абонент {user} удален")


def is_valid(user_input):
    result = re.match("^[А-я]{1,15} [А-я]{1,15} [А-я]{1,15} ((\+7|7|8)+([0-9]){10})$", user_input) is not None
    if not result and len(user_input) <= 12:
        return False
    else:
        return result


# удаление выделенного элемента
def delete():
    selection = subscribers_listbox.curselection()
    selected_subscriber = subscribers_listbox.get(selection[0])
    subscribers_listbox.delete(selection[0])
    selected_subscriber = selected_subscriber.split(' ')
    controller.dell_sub(selected_subscriber[3])
    dell_pass_massage(f'{selected_subscriber[0]} {selected_subscriber[1]}')


def find_subscriber():
    dell_subscriber = subscriber_entry_2.get()
    result = controller.get_subscriber_data(dell_subscriber)
    fill_list(result)


# добавление нового элемента
def add():
    new_subscriber = subscriber_entry.get()

    if not is_valid(new_subscriber):
        add_error_massage()
        return False
    else:
        result = controller.add_new_sub(new_subscriber)
        if result == -1:
            add_error_massage_2()
        else:
            subscriber_entry.delete(0, END)
            show_all_subscribers()
            new_subscriber = new_subscriber.split(" ")
            add_pass_massage(f'{new_subscriber[0]} {new_subscriber[1]}')


# Принемает массив строк и заполняет список
def fill_list(array):
    subscribers_listbox.delete(0, END)
    for el in array:
        subscribers_listbox.insert(END, el)


def show_all_subscribers():
    fill_list(controller.get_all_subscribers())


def clear_table():
    result = controller.truncate_table()
    if result:
        show_all_subscribers()
        truncate_pass()
    else:
        truncate_error()


# Класс окна
root = Tk()
root.title("Справочник ver 0.0.1")
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry('580x260+{}+{}'.format(int(x), int(y)))

# Добавляет строки и столбцы
root.columnconfigure(index=0, weight=2)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)
root.rowconfigure(index=3, weight=3)
root.rowconfigure(index=4, weight=1)

# текстовое поле и кнопка для добавления в список
subscriber_entry = ttk.Entry()
subscriber_entry.insert(0, "Фамилия Имя Отчество 89005553535")
subscriber_entry.grid(column=0, row=0, padx=6, pady=6, sticky=EW)

subscriber_entry_2 = ttk.Entry()
subscriber_entry_2.grid(column=0, row=2, padx=6, pady=6, sticky=EW)

ttk.Button(text="Добавить", command=add).grid(column=1, row=0, padx=6, pady=6, sticky=EW)
ttk.Button(text="Все абоненты", command=show_all_subscribers).grid(column=2, row=0, padx=6, pady=6, sticky=EW)
ttk.Button(text="Найти", command=find_subscriber).grid(column=1, row=2, padx=6, pady=6, sticky=EW)
ttk.Button(text="Очистить БД", command=clear_table).grid(column=2, row=2, padx=6, pady=6, sticky=EW)
ttk.Button(text="Удалить", command=delete).grid(row=3, column=1, padx=5, pady=5, sticky=EW)

# создаем список
subscribers_listbox = Listbox()
subscribers_listbox.grid(row=3, column=0, columnspan=1, sticky=EW, padx=5, pady=5)
