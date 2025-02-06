import tkinter as tk
from tkinter import ttk
import sqlite3
import pygame

# pygame для работы с аудио
pygame.init()
pygame.mixer.init()

# определение глобальных настроек шрифта и цветов
custom_font = ("Smeshariki Font", 16)
bg_color = "#FFA500"  # Оранжевый цвет для фона
button_color = "#FF8C00"  # Темно-оранжевый цвет для кнопок
entry_bg_color = "#FFFFFF"  # Белый цвет для полей ввода
frame_bg_color = "#FFB347"  # Более светлый оттенок оранжевого для фреймов


class CustomTitleBar(tk.Frame):  #кастомное управление, минимайз вырезал из за проблем, потом может починю
    def __init__(self, parent, close_cmd, minimize_cmd, maximize_cmd):
        super().__init__(parent, bg=bg_color, height=30)
        self.parent = parent
        self.create_widgets(close_cmd, minimize_cmd, maximize_cmd)
        self.bind_events()

    def create_widgets(self, close_cmd, minimize_cmd, maximize_cmd):
        self.pack(side=tk.TOP, fill=tk.X)

        self.close_img = tk.PhotoImage(file=r'C:\Users\RIfit\Desktop\Картинки для проекта\close_button.png')
        self.maximize_img = tk.PhotoImage(file=r'C:\Users\RIfit\Desktop\Картинки для проекта\maximize_button.png')

        self.close_button = tk.Button(self, image=self.close_img, command=close_cmd, bg=bg_color, bd=0)
        self.close_button.pack(side=tk.RIGHT, padx=5)

        self.maximize_button = tk.Button(self, image=self.maximize_img, command=maximize_cmd, bg=bg_color, bd=0)
        self.maximize_button.pack(side=tk.RIGHT, padx=5)

    #Настройки для перетаскивания окон
    def bind_events(self):
        self.bind('<Button-1>', self.on_press)
        self.bind('<B1-Motion>', self.on_drag)

    def on_press(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        x = self.parent.winfo_x() + (event.x - self._drag_start_x)
        y = self.parent.winfo_y() + (event.y - self._drag_start_y)
        self.parent.geometry(f'+{x}+{y}')


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.parent = parent
        self.main_app = main_app
        self.geometry("600x400+500+300")
        self.title("Вход в систему")
        self.resizable(False, False)
        self.init_login_window()

        # Скрыть стандартные кнопки
        self.overrideredirect(True)

        # кастомная панель управления приложением
        self.custom_title_bar = CustomTitleBar(self, self.close, self.minimize, self.maximize)

    # окно логина войти можно только по специальным данным)

    def init_login_window(self):
        frame = ttk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.logo_img = tk.PhotoImage(file=r'C:\Users\RIfit\Desktop\Картинки для проекта\logo.png') # Копатыч!
        logo_label = tk.Label(frame, image=self.logo_img)
        logo_label.pack(pady=10)

        ttk.Label(frame, text="Логин:", font=custom_font).pack(anchor=tk.W, padx=10)
        self.entry_login = ttk.Entry(frame, font=custom_font, background=entry_bg_color)
        self.entry_login.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame, text="Пароль:", font=custom_font).pack(anchor=tk.W, padx=10)
        self.entry_password = ttk.Entry(frame, show="*", font=custom_font, background=entry_bg_color)
        self.entry_password.pack(fill=tk.X, padx=10, pady=5)

        self.login_btn = ttk.Button(frame, text="Войти", command=self.check_login, style="Custom.TButton")
        self.login_btn.pack(pady=10)

        self.error_label = ttk.Label(frame, text="", foreground="red", font=custom_font)
        self.error_label.pack()

    def check_login(self):
        login = self.entry_login.get()
        password = self.entry_password.get()

        if login == "Копатыч" and password == "УкусиМеняПчола":
            self.error_label.config(text="")
            self.destroy()  # нет мейн окна
            self.main_app.show()  # мейн окно воркает
            self.main_app.play_success_sound()  # звук
        else:
            self.error_label.config(text="Неверный логин или пароль") # хз не воркает почему то

    def close(self): # штука для кастом управления
        self.destroy()

    def minimize(self): # штука для кастом управления
        self.iconify()

    def maximize(self): # штука для кастом управления
        if self.state() == 'normal':
            self.state('zoomed')
        else:
            self.state('normal')


class Main(tk.Frame):
    def __init__(self, root, db):
        super().__init__(root)
        self.db = db
        self.__init_main()
        self.pack(fill=tk.BOTH, expand=True)
        self.view_records()

    def show(self):
        self.master.deiconify()  # показ главного окна

    def play_success_sound(self):
        pygame.mixer.music.load(r'C:\Users\RIfit\Desktop\Картинки для проекта\success_sound.mp3') # проигрыш звука
        pygame.mixer.music.play()

    def open_dialog(self):
        Child(self)

    def open_update_dialog(self):
        Update(self)

    def search_records(self):
        query = self.entry_search.get()
        self.db.c.execute('''SELECT * FROM Honey WHERE name LIKE ?''', ('%' + query + '%',))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def __init_main(self):
        self.master.configure(bg=bg_color)  # фон окна

        # скрыть стандартные кнопки
        self.master.overrideredirect(True)

        # кастом системное управление шоб появилась
        self.custom_title_bar = CustomTitleBar(self.master, self.close, self.minimize, self.maximize)

        #тулбар(кнопки сверху)
        toolbar = tk.Frame(bg=frame_bg_color, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file=r'C:\Users\RIfit\Desktop\Картинки для проекта\add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить мёд', command=self.open_dialog, bg=button_color, bd=0,
                                    compound=tk.TOP, image=self.add_img, font=custom_font)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file=r'C:\Users\RIfit\Desktop\Картинки для проекта\update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', command=self.open_update_dialog, bg=button_color,
                                    bd=0,
                                    compound=tk.TOP, image=self.update_img, font=custom_font)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file=r'C:\Users\RIfit\Desktop\Картинки для проекта\delete.gif')
        btn_delete = tk.Button(toolbar, text='Утилизировать', command=self.delete_records, bg=button_color, bd=0,
                               compound=tk.TOP, image=self.delete_img, font=custom_font)
        btn_delete.pack(side=tk.LEFT)

        #  поле для поиска в тулбаре
        self.entry_search = ttk.Entry(toolbar, font=custom_font, background=entry_bg_color)
        self.entry_search.pack(side=tk.LEFT, padx=5)
        btn_search = ttk.Button(toolbar, text="Поиск", command=self.search_records, style="Custom.TButton")
        btn_search.pack(side=tk.LEFT)

        # скроллбар
        self.tree_frame = tk.Frame(self, bg=bg_color)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.tree_frame, columns=('АЙДИ', 'Описание', 'Колличество', 'Итого'),
                                 height=15, show='headings', yscrollcommand=self.tree_scroll.set)

        self.tree_scroll.config(command=self.tree.yview)

        # работа с колонками таблицы
        self.tree.column('АЙДИ', width=35, anchor=tk.CENTER)
        self.tree.column('Описание', width=365, anchor=tk.CENTER)
        self.tree.column('Колличество', width=150, anchor=tk.CENTER)
        self.tree.column('Итого', width=100, anchor=tk.CENTER)

        self.tree.heading('АЙДИ', text='Айди', anchor=tk.CENTER)
        self.tree.heading('Описание', text='Название мёду', anchor=tk.CENTER)
        self.tree.heading('Колличество', text='Имеется/съедено', anchor=tk.CENTER)
        self.tree.heading('Итого', text='Итого', anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

    # Для записи информации и не только
    def records(self, honeyname, money, total):
        self.db.insert_data(honeyname, money, total)
        self.view_records()

    def update_records(self, honeyname, money, total):
        self.db.c.execute('''UPDATE Honey SET name=?, costs=?, sum=? WHERE id=?''',
                          (honeyname, money, total, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.con.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM Honey''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM Honey WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.con.commit()
        self.view_records()

    def close(self):
        self.master.destroy()

    def minimize(self):
        self.master.iconify()

    def maximize(self):
        if self.master.state() == 'normal':
            self.master.state('zoomed')
        else:
            self.master.state('normal')


class Child(tk.Toplevel): # Дочерние окна
    def __init__(self, parent):
        super().__init__(parent)
        self.view = parent
        self.init_child()

    def init_child(self):
        self.title('Добавить мёд/убрать')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        self.configure(bg=bg_color)

        label_nemehoney = tk.Label(self, text='Название мёду:', font=custom_font, bg=bg_color)
        label_nemehoney.place(x=50, y=50)
        label_select = tk.Label(self, text='Имеется/съедено:', font=custom_font, bg=bg_color)
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Итого:', font=custom_font, bg=bg_color)
        label_sum.place(x=50, y=110)

        self.entry_namehoney = ttk.Entry(self, font=custom_font, background=entry_bg_color)
        self.entry_namehoney.place(x=200, y=50)

        self.entry_money = ttk.Entry(self, font=custom_font, background=entry_bg_color)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Имеется', u'Съедено'], font=custom_font)
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Отбой', command=self.destroy, style="Custom.TButton")
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Принято', style="Custom.TButton")
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_namehoney.get(),
                                                                       self.entry_money.get(),
                                                                       self.combobox.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self, parent):
        super().__init__(parent)

    def init_child(self):
        super().init_child()
        self.title('Редактировать мёд')

        btn_edit = ttk.Button(self, text='Редактировать', style="Custom.TButton")
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_namehoney.get(),
                                                                           self.entry_money.get(),
                                                                           self.combobox.get()))


class DB: # мне не зашло работать с SQL3
    def __init__(self):
        self.con = sqlite3.connect('honey.db')
        self.c = self.con.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Honey (id integer primary key, name text, costs text, sum real)''')
        self.con.commit()

    def insert_data(self, honeyname, money, total):
        self.c.execute('''INSERT INTO Honey(name, costs, sum) VALUES (?,?,?)''',
                       (honeyname, money, total))
        self.con.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()

    # Настройка стиля для кнопок
    style = ttk.Style()
    style.configure("Custom.TButton", font=custom_font, background=button_color)
    app = Main(root, db)

    # Сокрытие главного окна
    root.withdraw()

    # окно входа и ссылка на главное окно
    login_window = LoginWindow(root, app)

    # цикл проги, шоб случайно не делитнуть
    root.mainloop()

