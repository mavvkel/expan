import customtkinter as ctk
from main import dispenser

def load_exp_data(frame):
    #exp_labels = []
    dispenser.to_next()
    row = dispenser.current()

    date_label = ctk.CTkLabel(master=frame,
                              text=row.iloc[0])
    receiver_label = ctk.CTkLabel(master=frame,
                                  text=row.iloc[1])
    title_label = ctk.CTkLabel(master=frame,
                               text=row.iloc[2])
    amount_label = ctk.CTkLabel(master=frame,
                                text=row.iloc[3])

    date_label.grid(row=0, column=0)
    receiver_label.grid(row=0, column=1)
    title_label.grid(row=0, column=2)
    amount_label.grid(row=0, column=3)
    # for i, row in exps.iterrows():
    #    #exp_labels.append(label);
    #    #label.pack()

def load_next_expense(frame):
    pass



root = ctk.CTk()
root.geometry(geometry_string="1700x1000+0+0")
root.title(string="Expan")

frame = ctk.CTkScrollableFrame(master=root,
                               width=1600,
                               height=800)
frame.grid_rowconfigure(index=0,
                        weight=1)
frame.grid_columnconfigure(index=0,
                           weight=1)
frame.grid_columnconfigure(index=1,
                           weight=1)
frame.grid_columnconfigure(index=2,
                           weight=1)
frame.grid_columnconfigure(index=3,
                           weight=1)
frame.pack(padx=50, pady=50)

load_exp_data(frame);

root.mainloop()





