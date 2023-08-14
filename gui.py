from typing import Optional, Tuple, Union

import customtkinter as ctk
from PIL import Image

from main import dispenser


class App(ctk.CTk):
    # TODO: refactor frame loading
    # TODO: those should be instance vars
    current_frame = None
    frame = None
    date_label = None
    receiver_label = None
    title_label = None
    amount_label = None
    processed_labels = []
    indicator_imgs = []
    categories = ['eatout',
                  'groceries',
                  'leisure',
                  'clothing',
                  'shopping',
                  'transport',
                  'dance',
                  'media',
                  'misc',
                  'rent']


    def __init__(self, fg_color: Optional[Union[str, Tuple[str, str]]] =
                 None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry(geometry_string="1300x1000+0+0")
        self.title(string="Expan")
        self.configure(fg_color='#34343D')
        

        # previous expenses frame
        self.frame = ctk.CTkScrollableFrame(master=self,
                                            width=1200,
                                            height=220,
                                            fg_color='#2A2A32')
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
                                          height=100,
                                          fg_color='#2A2A32')
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
        self.current_frame.pack(padx=25,
                                pady=(0, 25))
        self.current_frame.grid_propagate(False)


        # labels in current expense frame
        self.date_label = ctk.CTkLabel(master=self.current_frame)
        self.receiver_label = ctk.CTkLabel(master=self.current_frame)
        self.title_label = ctk.CTkLabel(master=self.current_frame)
        self.amount_label = ctk.CTkLabel(master=self.current_frame)

        self.load_progress_bar()
        self.load_category_buttons()
        self.load_cat_indicator_imgs()

        self.bind_keyboard_shortcuts()

        self.load_next()


    def bind_keyboard_shortcuts(self):
        if len(App.categories) < 11: # with more the seq concat will break
            for i in range(len(App.categories)):
                seq = '<Key-' + str((i + 1) % 10) + '>'
                self.bind(seq, lambda _, category = i + 1:
                          self.load_next(category))
        else:
            raise NotImplementedError


    def load_category_buttons(self):
        bt_size = 70

        # setup category frame & its grid
        self.cat_frame = ctk.CTkFrame(master=self,
                                      width=1220,
                                      height=1*bt_size + 20,
                                      fg_color='#2A2A32')
        self.cat_frame.grid_rowconfigure(index=0,
                                         weight=1)
        for col in range(len(App.categories)):
            self.cat_frame.grid_columnconfigure(index=col,
                                                weight=1)
        self.cat_frame.pack(padx=25,
                            pady=25)
        self.cat_frame.grid_propagate(False)


        # load images and their buttons
        for i, name in enumerate(App.categories):
            bt_path = 'static/icons/' + name + '_button.png'
            bt_img = ctk.CTkImage(Image.open(bt_path),
                                     size=(bt_size, bt_size))
            bt = ctk.CTkButton(master=self.cat_frame,
                               image=bt_img,
                               width=0,
                               height=0,
                               fg_color="transparent",
                               text="",
                               hover=False,
                               command=lambda category=i + 1:
                               self.load_next(category))
            bt.grid(column=i, row=0)


    def load_cat_indicator_imgs(self):
        ind_size = 18

        for name in App.categories:
            ind_path = 'static/icons/' + name + '_cat_indicator.png'
            self.indicator_imgs.append(ctk.CTkImage(Image.open(ind_path),
                                                    size=(ind_size, ind_size)))


    def load_progress_bar(self):
        self.progress_label = ctk.CTkLabel(master=self,
                                           text='0 / ' + str(dispenser.length()))
        self.progress_label.pack(pady=(0, 5))
        self.progress_bar = ctk.CTkProgressBar(master=self,
                                               width=500,
                                               height=8,
                                               fg_color='white',
                                               progress_color='#0E95F6',
                                               mode='determinate',
                                               determinate_speed=50.0 /
                                               dispenser.length())
        self.progress_bar.set(0.0)
        self.progress_bar.pack(padx=25,
                               pady=25)


    def save_current(self, category):
        if category is not None:
            dispenser.assign_current(category=category)
            self.progress_bar.step()


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
                                          image=self.indicator_imgs[
                                              last.loc['category'] - 1])
            
            if last.loc['Kwota'].startswith('-'):
                amount_label.configure(text_color='red')
            else:
                amount_label.configure(text_color='green')

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

        if dispenser.to_next():
            self.progress_label.configure(text=str(dispenser.current_index + 1) 
                                          + ' / ' + str(dispenser.length()))

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
            self.date_label.configure(text='----')
            self.receiver_label.configure(text='----')
            self.title_label.configure(text='----')
            self.amount_label.configure(text='----')
            self.amount_label.configure(text_color='white')

            dispenser.save_processed()
            

        self.date_label.grid(row=0, column=0)
        self.receiver_label.grid(row=0, column=1)
        self.title_label.grid(row=0, column=2)
        self.amount_label.grid(row=0, column=3)

        self.load_last_processed()

        self.frame.update_idletasks()
        self.frame._parent_canvas.yview_moveto('1.0')


app = App()
app.mainloop()

