from operator import index
import customtkinter as ctk
from dispenser import Dispenser
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
    processed_labels = []
    indicator_imgs = []

    def __init__(self, fg_color: Optional[Union[str, Tuple[str, str]]] = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry(geometry_string="1300x1000+0+0")
        self.title(string="Expan")


        # previous expenses frame
        self.frame = ctk.CTkScrollableFrame(master=self,
                                            width=1200,
                                            height=220)
        self.frame.grid_rowconfigure(index=0,
                                     weight=1)
        self.frame.grid_columnconfigure(index=0,
                                        weight=1)
        self.frame.grid_columnconfigure(index=1,
                                        weight=1)
        self.frame.grid_columnconfigure(index=2,
                                        weight=1)
        self.frame.grid_columnconfigure(index=3,
                                        weight=1)
        self.frame.pack(padx=25,
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

        
        # init indicator icon images
        self.indicator_imgs.append(ctk.CTkImage(Image.open("static/icons/dance_category_indicator.png"),
                                                size=(18, 18)))
        self.indicator_imgs.append(ctk.CTkImage(Image.open("static/icons/groceries_category_indicator.png"),
                                                size=(18, 18)))



    def save_current(self, category):
        if category != None:
            dispenser.assign_current(category=category)


    def load_last_processed(self):
        last = dispenser.get_last_processed()

        if last is not None:
            date_label = ctk.CTkLabel(master=self.frame,
                                      text=last.loc['Data transakcji'])
            receiver_label = ctk.CTkLabel(master=self.frame,
                                      text=last.loc['Dane kontrahenta'][0:40])
            title_label = ctk.CTkLabel(master=self.frame,
                                      text=last.loc['Tytuł'][0:70])
            amount_label = ctk.CTkLabel(master=self.frame,
                                      text=last.loc['Kwota'])
            category_label = ctk.CTkLabel(master=self.frame,
                                          text='',
                                          image=self.indicator_imgs[last.loc['category'] - 1])
            

            date_label.grid(column=0)
            this_row = date_label.grid_info()['row']
            receiver_label.grid(row=this_row, column=1)
            title_label.grid(row=this_row, column=2)
            amount_label.grid(row=this_row, column=3, padx=10)
            category_label.grid(row=this_row, column=4, padx=20)
            


        # for i, row in dispenser.get_processed().iterrows():
        #     self.processed_labels.append(label)
        #     print(i)
        #     print(self.processed_labels)
        #     self.processed_labels[i].grid(row=i, column=0)


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

        self.load_last_processed()

        self.frame.update_idletasks()
        self.frame._parent_canvas.yview_moveto('1.0')


app = App()
app.mainloop()


"""

1. load_next to the current frame
2. click category button
3. save the category
4. load the saved expense and its category to the processed frame
5. load_next to the current frame

"""
