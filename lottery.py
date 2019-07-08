import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

LARGE_FONT = ("Roboto", 20)
TICKET_FONT = ("Roboto", 240)

class Lottery(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Loterij")
        self.ticket_numbers = np.array([])
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageTicketRanges, PageIncome, PageTicketDraw):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.ticket_ranges = []

        self.show_frame(PageTicketRanges)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()

    def money_validation(self, S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',']:
            return True
        self.bell()
        return False

    def integer_validation(self, S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True
        self.bell()
        return False


class PageTicketRanges(tk.Frame):

    def create_tickets(self):
        ticket_ranges = []
        for entry in self.entry_ticket_ranges:
            from_value = entry[0].get()
            to_value = entry[1].get()
            if from_value != '' and to_value != '':
                ticket_ranges.append([int(from_value), int(to_value)])
            elif from_value != '' and to_value == '':
                ticket_ranges.append(int(from_value))
            elif from_value == '' and to_value != '':
                messagebox.showinfo("Fout", "Er kan niet alleen een eindpunt van een range worden opgegeven")
                return

        for ticket_range in ticket_ranges:
            self.controller.ticket_numbers = np.append(self.controller.ticket_numbers,
                                                       np.arange(ticket_range[0], ticket_range[1] + 1))

        self.controller.show_frame(PageIncome)

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        range_sets = ['Set 1', 'Set 2', 'Set 3', 'Set 4', 'Set 5', 'Set 6']

        vcmd = (self.register(controller.integer_validation), '%S')
        self.entry_ticket_ranges = []
        for range_set in range_sets:
            frame = tk.Frame(self)
            label = tk.Label(frame, text=range_set, relief=tk.RIDGE,  width=25)
            entry_from = tk.Entry(frame, relief=tk.SUNKEN, width=50, justify='right',
                                  validate='key', vcmd=vcmd)
            entry_to = tk.Entry(frame, relief=tk.SUNKEN, width=50, justify='right',
                                validate='key', vcmd=vcmd)
            self.entry_ticket_ranges.append([entry_from, entry_to])
            frame.pack(side=tk.TOP)
            label.pack(side=tk.LEFT)
            entry_from.pack(side=tk.LEFT)
            entry_to.pack(side=tk.RIGHT)

        btn_start = tk.Button(self, text='Bereken inkomsten >',
                              command=self.create_tickets)
        btn_start.pack()


class PageIncome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)
        self.ticket_numbers = self.controller.ticket_numbers

        btn_exit = tk.Button(self, text='< Terug naar lot sets',
                             command=lambda: controller.show_frame(PageTicketRanges))
        btn_exit.pack()

        self.label = tk.Label(self, text="Geen loten verkocht", font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)

        vcmd = (self.register(controller.money_validation), '%S')
        self.entry_price = tk.Entry(self, relief=tk.SUNKEN, width=50, justify='right',
                                    validate='key', vcmd=vcmd)
        self.entry_price.pack()

        btn_calculate = tk.Button(self, text='Bereken inkomsten',
                                  command=self.calculate_income)
        btn_calculate.pack()

        self.label_income = tk.Label(self, text="Geen inkomsten", font=LARGE_FONT)
        self.label_income.pack(pady=10, padx=10)

        btn_start = tk.Button(self, text='Start loterij >',
                              command=lambda: controller.show_frame(PageTicketDraw))
        btn_start.pack()

    def on_show_frame(self, event):
        self.ticket_numbers = self.controller.ticket_numbers
        qty_tickets = self.ticket_numbers.shape[0]
        self.label['text'] = 'Aantal verkochte loten: ' + str(qty_tickets)

    def calculate_income(self):
        qty_tickets = self.ticket_numbers.shape[0]
        amt_price = float(self.entry_price.get().replace(',', '.'))
        amt_income = qty_tickets * amt_price
        amt_income = ('%.2f' % amt_income).replace('.', ',')
        self.label_income['text'] = 'Inkomsten loten verkoop : €' + amt_income


class PageTicketDraw(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.qty_draws = 0

        self.label_ticket = tk.Label(self, text=" ", font=TICKET_FONT)
        self.label_ticket.pack(pady=10, padx=10)

        self.btn_draw = tk.Button(self, text='Volgende lot',
                                  command=self.draw_ticket)
        self.btn_draw.pack()

    def draw_ticket(self):
        qty_tickets = self.controller.ticket_numbers.shape[0]
        if qty_tickets > 0:
            self.qty_draws = self.qty_draws + 1

            idx_ticket = random.randint(0, qty_tickets - 1)
            drawn_ticket = self.controller.ticket_numbers[idx_ticket]
            self.controller.ticket_numbers = np.delete(self.controller.ticket_numbers,
                                                       idx_ticket)
            self.label_ticket['text'] = int(drawn_ticket)
        else:
            self.label_ticket['font'] = LARGE_FONT
            self.label_ticket['text'] = 'De loten zijn op.'
            self.label_ticket['text'] = 'Stop de loterij'
            self.label_ticket['command'] = self.controller.destroy

app = Lottery()
app.mainloop()


#     btn_start = Button(frame_bottom, text='Start loterij', command=form_lottery_close)

