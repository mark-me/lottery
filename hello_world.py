import tkinter as tk
import numpy as np

LARGE_FONT = ("Roboto", 20)


class Lottery(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Loterij")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.ticket_ranges = []

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start page", font=LARGE_FONT)
        colors = ['red', 'green', 'yellow', 'orange', 'blue', 'navy']
        for c in colors:
            frame = tk.Frame(self)
            label = tk.Label(frame, text=c, relief=tk.RIDGE,  width=25)
            entry_from = tk.Entry(frame, relief=tk.SUNKEN, width=50)
            entry_to = tk.Entry(frame, relief=tk.SUNKEN, width=50)
            frame.pack(side=tk.TOP)
            label.pack(side=tk.LEFT)
            entry_from.pack(side=tk.LEFT)
            entry_to.pack(side=tk.RIGHT)
            controller.ticket_ranges.append([entry_from, entry_to])

        btn_start = tk.Button(self, text='Start loterij',
                              command=lambda: controller.show_frame(PageOne))
        btn_start.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Loterij pagina", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        btn_exit = tk.Button(self, text='Terug naar ticket verkoop',
                             command=lambda: controller.show_frame(StartPage))
        btn_exit.pack()


app = Lottery()
app.mainloop()


#     btn_start = Button(frame_bottom, text='Start loterij', command=form_lottery_close)

