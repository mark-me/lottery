import tkinter as tk
import random

import numpy as np

from config_ui import LARGE_FONT, TICKET_FONT

class PageTicketDraw(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.qty_draws = 0

        frame_btns = tk.Frame(self)
        frame_btns.pack(side=tk.TOP, fill=tk.X, expand=0)
        self.btn_draw = tk.Button(frame_btns, text="Trek lot", command=self.draw_ticket)
        self.btn_draw.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.btn_quit = tk.Button(
            frame_btns, text="Stop loterij", command=self.controller.destroy
        )
        self.btn_quit.pack(side=tk.RIGHT, fill=tk.X, expand=1)

        self.label_ticket = tk.Label(self, text=" ", font=TICKET_FONT)
        self.label_ticket.pack(fill=tk.BOTH, expand=1)

    def draw_ticket(self):
        qty_tickets = self.controller.ticket_numbers.shape[0]
        if qty_tickets > 0:
            self.qty_draws = self.qty_draws + 1

            idx_ticket = random.randint(0, qty_tickets - 1)
            drawn_ticket = self.controller.ticket_numbers[idx_ticket]
            self.controller.ticket_numbers = np.delete(
                self.controller.ticket_numbers, idx_ticket
            )
            self.label_ticket["text"] = int(drawn_ticket)
        else:
            self.label_ticket["font"] = LARGE_FONT
            self.label_ticket["text"] = "De loten zijn op."
            self.qty_draws = 0
            tk.messagebox.showinfo("Loterij", "De loten zijn op. Sluit het programma af")
            self.btn_draw.pack_forget()

    def quit_lottery(self):
        if tk.messagebox.askokcancel(
            "Exit", "Weet je zeker dat je het programma wil afsluiten?"
        ):
            self.controller.destroy()

