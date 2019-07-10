import tkinter as tk
import numpy as np
from tkinter import messagebox
import random

LARGE_FONT = ("Roboto", 20)
TICKET_FONT = ("Roboto", 240)


class Lottery(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Loterij")
        self.ticket_numbers = np.array([])
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.state("zoomed")

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

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        range_sets = ['Set 1', 'Set 2', 'Set 3', 'Set 4', 'Set 5', 'Set 6']

        label = tk.Label(self, text="Geef lotensets op", font=LARGE_FONT)
        label.pack(side=tk.TOP, fill="x", pady=10)

        frame_filler_top = tk.Frame(self)
        frame_filler_top.pack(side=tk.TOP, fill=tk.Y, expand=1)

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
            frame.pack(side=tk.TOP, fill=tk.Y)
            label.pack(side=tk.LEFT)
            entry_from.pack(side=tk.LEFT)
            entry_to.pack(side=tk.RIGHT)

        frame_filler_btm = tk.Frame(self)
        frame_filler_btm.pack(side=tk.TOP, fill=tk.Y, expand=1)

        btn_start = tk.Button(self, text='Ga naar berekenen inkomsten >',
                              command=self.create_tickets)
        btn_start.pack(side=tk.BOTTOM, fill=tk.X)

    def create_tickets(self):

        # Create ticket ranges
        self.controller.ticket_numbers = np.array([])
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

        # Create tickets
        for ticket_range in ticket_ranges:
            self.controller.ticket_numbers = np.append(self.controller.ticket_numbers,
                                                       np.arange(ticket_range[0], ticket_range[1] + 1))

        if np.unique(self.controller.ticket_numbers).shape[0] != self.controller.ticket_numbers.shape[0]:
            messagebox.showinfo("Fout", "Er kunnen geen overlappende ranges worden opgegeven")
            return

        self.controller.show_frame(PageIncome)


class PageIncome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)
        self.ticket_numbers = self.controller.ticket_numbers

        btn_exit = tk.Button(self, text='< Terug naar lot sets',
                             command=lambda: controller.show_frame(PageTicketRanges))
        btn_exit.pack(side=tk.TOP, fill=tk.X, expand=0)

        frame_sold_qty = tk.Frame(self)
        frame_sold_qty.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.label = tk.Label(frame_sold_qty, text="Geen loten verkocht", font=LARGE_FONT)
        self.label.pack(fill=tk.BOTH, expand=1)

        frame_price = tk.Frame(self)
        frame_price.pack(side=tk.TOP, fill=tk.Y, expand=1)
        label_price = tk.Label(frame_price, text="Prijs per lot: ", relief=tk.RIDGE,  width=15)
        label_price.pack(side=tk.LEFT)
        vcmd = (self.register(controller.money_validation), '%S')
        self.entry_price = tk.Entry(frame_price, relief=tk.SUNKEN, width=25, justify='right',
                                    validate='key', vcmd=vcmd)
        self.entry_price.pack(side=tk.LEFT, fill=tk.X, expand=0)
        btn_calculate = tk.Button(frame_price, text='Bereken inkomsten',
                                  command=self.calculate_income)
        btn_calculate.pack(side=tk.RIGHT, fill=tk.X, expand=0)

        frame_price_total = tk.Frame(self)
        frame_price_total.pack(side=tk.TOP, fill=tk.Y, expand=1)
        self.label_income = tk.Label(frame_price_total, text="Geen inkomsten", font=LARGE_FONT)
        self.label_income.pack(fill=tk.BOTH, expand=1)

        btn_start = tk.Button(self, text='Start loterij >',
                              command=lambda: controller.show_frame(PageTicketDraw))
        btn_start.pack(side=tk.BOTTOM, fill=tk.X)

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

        frame_btns = tk.Frame(self)
        frame_btns.pack(side=tk.TOP, fill=tk.X, expand=0)
        self.btn_draw = tk.Button(frame_btns, text='Trek lot',
                                  command=self.draw_ticket)
        self.btn_draw.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.btn_quit = tk.Button(frame_btns, text='Stop loterij',
                                  command=self.draw_ticket)
        self.btn_quit.pack(side=tk.RIGHT, fill=tk.X, expand=1)

        self.label_ticket = tk.Label(self, text=" ", font=TICKET_FONT)
        self.label_ticket.pack(fill=tk.BOTH, expand=1)

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
            self.btn_draw['text'] = '<< Start loterij opnieuw'
            self.btn_draw['command'] = self.controller.show_frame(PageTicketRanges)

    def quit_lottery(self):
        if messagebox.askokcancel("Exit", "Weet je zeker dat je het programma wil afsluiten?"):
            self.controller.destroy()


def main():
    app = Lottery()
    app.mainloop()


if __name__ == '__main__':
    main()