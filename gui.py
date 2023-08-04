import customtkinter as ctk
from main import dispenser
from typing import Optional, Union, Tuple
from PIL import Image


class App(ctk.CTk):
    current_frame = None
    frame = None
    date_label = None
    receiver_label = None
    title_label = None
    amount_label = None

    def __init__(self, fg_color: Optional[Union[str, Tuple[str, str]]] = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry(geometry_string="1700x1000+0+0")
        self.title(string="Expan")


        # previous expenses frame
        self.frame = ctk.CTkScrollableFrame(master=self,
                                            width=1200)
        self.frame.grid_rowconfigure(index=0,
                                     weight=1)
        self.frame.grid_columnconfigure(index=0,
                                        weight=0)
        self.frame.grid_columnconfigure(index=1,
                                        weight=0)
        self.frame.grid_columnconfigure(index=2,
                                        weight=0)
        self.frame.grid_columnconfigure(index=3,
                                        weight=0)
        self.frame.pack(padx=50,
                        pady=25)


        # current expense frame
        self.current_frame = ctk.CTkFrame(master=self,
                                          width=1220,
                                          height=100)
        self.current_frame.grid_rowconfigure(index=0,
                                             weight=1)
        self.current_frame.grid_columnconfigure(index=0,
                                                weight=1)
        self.current_frame.grid_columnconfigure(index=1,
                                                weight=1)
        self.current_frame.grid_columnconfigure(index=2,
                                                weight=1)
        self.current_frame.grid_columnconfigure(index=3,
                                                weight=1)
        self.current_frame.pack(padx=50,
                                pady=25)
        self.current_frame.grid_propagate(False)


        # labels in current expense frame
        self.date_label = ctk.CTkLabel(master=self.current_frame)
        self.receiver_label = ctk.CTkLabel(master=self.current_frame)
        self.title_label = ctk.CTkLabel(master=self.current_frame)
        self.amount_label = ctk.CTkLabel(master=self.current_frame)

        
        # category buttons
        dance_image = ctk.CTkImage(Image.open("static/icons/dance_button.png"),
                                   size=(70, 70))
        dance_bt = ctk.CTkButton(master=self,
                                 image=dance_image,
                                 width=0,
                                 height=0,
                                 fg_color="transparent",
                                 text="",
                                 hover=False,
                                 command=lambda: self.load_next(1))
        dance_bt.pack()
        groceries_image = ctk.CTkImage(Image.open("static/icons/groceries_button.png"),
                                       size=(70, 70))
        groceries_bt = ctk.CTkButton(master=self,
                                 image=groceries_image,
                                 width=0,
                                 height=0,
                                 fg_color="transparent",
                                 text="",
                                 hover=False,
                                 command=lambda: self.load_next(2))
        groceries_bt.pack(pady=10)

        self.load_next()


    def save_current(self, category):
        if category != None:
            dispenser.assign_current(category=category)


    def load_next(self, category = None):
        self.save_current(category)

        row = None
        if dispenser.to_next():
            row = dispenser.current()
            self.date_label.configure(text=row['Data transakcji'])
            self.receiver_label.configure(text=row['Dane kontrahenta'])
            self.title_label.configure(text=row['Tytuł'])
            self.amount_label.configure(text=row['Kwota'])

            if row['Kwota'].startswith('-'):
                self.amount_label.configure(text_color='red')
            else:
                self.amount_label.configure(text_color='green')

        else:
            print('That\'s all')
            self.date_label.configure(text='----')
            self.receiver_label.configure(text='----')
            self.title_label.configure(text='----')
            self.amount_label.configure(text='----')
            self.amount_label.configure(text_color='white')
            

        self.date_label.grid(row=0, column=0)
        self.receiver_label.grid(row=0, column=1)
        self.title_label.grid(row=0, column=2)
        self.amount_label.grid(row=0, column=3)
        # for i, row in exps.iterrows():
        #    #exp_labels.append(label);
        #    #label.pack()

    

app = App()
app.mainloop()


"""

1. load_next to the current frame
2. click category button
3. save the category
4. load the saved expense and its category to the processed frame
5. load_next to the current frame

"""
