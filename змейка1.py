from tkinter import Tk, Canvas, messagebox, Label
import tkinter as tk
import random

# размерность
WIDTH = 900
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True
paused = False

def pause():
    global paused, continue_button, pause_button
    paused = not paused
    pause_button.place_forget()
    continue_button.place(relx=0.62, rely=0.92)

# вспомогательные функции
def create_block():
    # создание еды, которую нужно съесть
    global BLOCK
    while True:
        posx = SEG_SIZE * random.randint(1, int((WIDTH-SEG_SIZE) / SEG_SIZE))
        posy = SEG_SIZE * random.randint(1, int((HEIGHT-SEG_SIZE) / SEG_SIZE))
        overlapping_items = c.find_overlapping(posx, posy, posx + SEG_SIZE, posy + SEG_SIZE)
        overlapping = False
        for item in overlapping_items:
            if "snake" in c.gettags(item):
                overlapping = True
                break
        if not overlapping:
            break
    BLOCK = c.create_oval(posx, posy, posx+SEG_SIZE, posy+SEG_SIZE, fill="yellow")
    return BLOCK

def main():
    global IN_GAME, score, paused
    while IN_GAME:
        # обработка игрового процесса
        if not paused:
            s.move()
            head_coords = c.coords(s.segments[-1].instance)
            x1, y1, x2, y2 = head_coords
            # проверка границ с краями игрового поля
            if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
                IN_GAME = False
                root.bind("<Return>", clicked)
            # змейка есть еду
            elif head_coords == c.coords(BLOCK):
                s.add_segment()
                c.delete(BLOCK)
                create_block()
                score += 10
                schet['text'] = f'Счет: {score}'
            # самопоедание
            else:
                for index in range(len(s.segments)-1):
                    if head_coords == c.coords(s.segments[index].instance):
                        IN_GAME = False
                        root.bind("<Return>", clicked)
                        break
        # если не в игре - остановить игру и вывести сообщение
        if not IN_GAME:
            paused = True
            schet['text'] = f'Счет: {0}'
            continue_button.place_forget()
            pause_button.place_forget()
            end_label.place(relx=0.5, rely=0.4, anchor="center")
            end1_label.place(relx=0.5, rely=0.55, anchor="center")

        root.update()  # обновление окна
        root.after(100)  # задержка


class Segment(object):
    # один сегмент змеи
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x+SEG_SIZE, y+SEG_SIZE,
                                           fill="white", tags="snake")


class Snake(object):
    # простой класс змейки
    def __init__(self, segments):
        self.segments = segments
        # возможные ходы
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # начальное направление движения
        self.vector = self.mapping["Right"]

    def move(self):
        # перемещение змейки с указанным вектором
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

    def add_segment(self):
        # добавляет сегмент к змейке
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        # изменяет направление змейки
        if event.keysym in self.mapping and event.keysym:
            new_vector = self.mapping[event.keysym]
            opposite_vector = tuple(map(lambda x: -x, self.vector))
            if new_vector != opposite_vector:
                self.vector = new_vector

    def reset_snake(self):
        root.unbind("<Return>")
        for segment in self.segments:
            c.delete(segment.instance)

def set_state(item, state):
    c.itemconfigure(item, state=state)

def clicked(event):
    global IN_GAME, paused
    paused = False
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    c.delete(BLOCK)
    c.delete(BLOCK)
    end_label.place_forget() # скрываем текст
    end1_label.place_forget()
    start_game()

def disable_tab(event):
    # отключает выбор кнопки с помощью клавиши Tab
    global tab_allowed
    tab_allowed = False
    return "break"

def menu():
    global root, c, start_button, quit_button, pravila_button, schet, menu_button, \
    pause_button, continue_button, end_label, end1_label, game_title

    # создаем окно программы
    root = Tk()
    root.iconphoto(True, tk.PhotoImage(file="icon1.png"))
    root.title("Змейка")
    root.geometry("900x650")
    root["bg"] = '#FFFFFF'

    c = Canvas(root, width=900, height=600, bg="#000000", highlightthickness=0)
    c.place(relx=0.5, rely=0.45, anchor="center")

    game_title = Label(root, text="Змейка", font='Arial 25', bg='black', fg='white')
    game_title.place(relx=0.5, rely=0.1, anchor="center")

    end_label = Label(root, text="КОНЕЦ ИГРЫ", bg='black', font="Arial 30", fg='red')
    end1_label = Label(root, text="Нажмите Enter, чтобы начать заново", bg='black', font="Arial 25", fg='white')
    schet = tk.Label(root, text=f'Счет: {0}', bg='white', font='Arial 25')

    # перехватывать нажатие клавиш
    c.focus_set()
    root.bind("<Tab>", disable_tab)

    # функции для кнопок
    def quit_game():
        root.destroy()

    def pravila():
        messagebox.showinfo( title= "Змейка", message='                            Правила игры "Змейка"'
                                 '\n'
                                 '\n    Для того чтобы управлять змейкой выбирайте кнопки клавиатуры "стрелки" (вверх, вниз, влево, вправо).'
                                    '\n'
                                    '\n    Для запуска игры используйте кнопку "Начать игру".'
                                    '\n'
                                    '\n     После каждого съеденного объекта количество очков и размер змейки увеличивается. Игрок проиграет, если змейка наедет сама на себя или ударится о границы поля.'
                                    '\n'
                                    '\n     Если необходимо остановить игру, используйте кнопку "Пауза" на игровом поле.'
                                    '\n'
                                    '\n     Выход из игры осуществляется через полное закрытие программы или через кнопку "Выйти из игры" в меню игры.'
                                    '\n'
                                    '\n                                           Удачи!')


    # создаем кнопки
    start_button = tk.Button(root, text="Начать игру", bg='#E6E6FA', foreground='black', font='Arial 16', width=15,
                             height=1, command=start_game)
    start_button.place( relx=0.5, rely=0.2, anchor="center")

    quit_button = tk.Button(root,text="Выйти из игры", bg='#E6E6FA', foreground='black', font='Arial 16', width=15,
                            height=1, command=quit_game)

    quit_button.place( relx=0.5, rely=0.3, anchor="center")
    pravila_button = tk.Button(root,text='Правила игры', bg='#E6E6FA', foreground='black', font='Arial 16', width=15,
                               height=1, command=pravila)
    pravila_button.place( relx=0.5, rely=0.4, anchor="center")

    menu_button = tk.Button(root, text='Главная', bg='#E6E6FA', foreground='black', font='Arial 16', width=15,
                               height=1, command=return_menu)
    menu_button.place(relx=0.22, rely=0.92)
    menu_button.place_forget()

    pause_button = tk.Button(root, text='Пауза', bg='#E6E6FA', foreground='black', font='Arial 16', width=15,
                               height=1, command=pause)
    pause_button.place(relx=0.62, rely=0.93)
    pause_button.place_forget()

    continue_button = tk.Button(root, text='Продолжить', bg='#FF0000', foreground='black', font='Arial 16', width=15,
                             height=1, command=not_pause)
    continue_button.place(relx=0.62, rely=0.92)
    continue_button.place_forget()

    end_label.place_forget()
    end1_label.place_forget()

    # запуск окна программы
    root.mainloop()

def not_pause():
    global paused
    paused = False
    continue_button.place_forget()
    pause_button.place(relx=0.62, rely=0.92)

def return_menu():
    global score, IN_GAME
    IN_GAME = False
    root.unbind("<Return>")
    end_label.place_forget()
    end1_label.place_forget()
    game_title.place(relx=0.5, rely=0.1, anchor="center")
    menu_button.place_forget()
    score = 0
    schet['text'] = f'Счет: {score}'
    schet.place_forget()
    start_button.place(relx=0.5, rely=0.2, anchor="center")
    quit_button.place(relx=0.5, rely=0.3, anchor="center")
    pravila_button.place(relx=0.5, rely=0.4, anchor="center")
    continue_button.place_forget()
    pause_button.place_forget()
    c.delete(BLOCK)
    s.reset_snake()

def start_game():
    global s, score, IN_GAME, paused
    IN_GAME = True
    paused = False
    start_button.place_forget()
    quit_button.place_forget()
    pravila_button.place_forget()
    game_title.place_forget()
    menu_button.place(relx=0.22, rely=0.92)
    pause_button.place(relx=0.62, rely=0.92)
    pause_button.place(relx=0.62, rely=0.92)
    score = 0
    schet.place(relx=0.45, rely=0.92)
    create_block()
    s = create_snake()
    # реакция на нажатие клавиши
    c.bind("<KeyPress>", s.change_direction)
    main()

def create_snake():
    # создание сегментов и змейки
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE*2, SEG_SIZE),
                Segment(SEG_SIZE*3, SEG_SIZE)]
    return Snake(segments)


menu()