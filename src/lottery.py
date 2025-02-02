import tkinter as tk

import numpy as np

from pages_sell_tickets import PageTicketRanges, PageIncome
from page_ticket_draw import PageTicketDraw

class Lottery(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Loterij")
        self.ticket_numbers = np.array([])
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.state("normal")

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
        if S in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ","]:
            return True
        self.bell()
        return False

    def integer_validation(self, S):
        if S in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return True
        self.bell()
        return False



