import pandas as pd
import numpy as np


"""
"""
class Dispenser:

    def __init__(self, file):
        self.file = file
        self.current_index = -1
        self.processed = []


        # todo: error checking for fail on open
        # load expenses
        self.df = pd.read_csv(filepath_or_buffer=file,
                              sep=';',
                              header=11,
                              encoding='ansi',
                              on_bad_lines='skip',
                              usecols=range(0, 15))
        Dispenser.clean_df_from_ing(self.df)


        # load first entry
        # self.current_index = 0
        # print(self.df.iloc[self.current_index])


    @staticmethod
    def clean_df_from_ing(exps):
        exps.drop(columns=['Data księgowania', 'Nr rachunku', 'Nazwa banku',
                           'Nr transakcji', 'Waluta', 'Waluta.1', 'Waluta.2',
                           'Kwota płatności w walucie'], inplace=True)


        # last row is some note
        exps.drop(index=exps.index[-1],
                  axis=0,
                  inplace=True)


        # strip redunant transactions
        exps.drop(index=exps[exps['Tytuł'].str.contains('Own transfer')].index,
                  axis=0,
                  inplace=True)
        exps.drop(index=exps[exps['Tytuł'].str.contains('Przelew własny')].index,
                  axis=0,
                  inplace=True)


        # compress 3 money columns into 1
        exps['Kwota'] = np.where(exps['Szczegóły'].isna() | 
                                 exps['Szczegóły'].str.isspace(),
                                 exps['Kwota transakcji (waluta rachunku)'],
                                 exps['Szczegóły'])
        exps['Kwota'] = np.where(exps['Kwota'].isnull(),
                                 exps['Kwota blokady/zwolnienie blokady'],
                                 exps['Kwota'])
        exps = exps.drop(columns=['Szczegóły',
                                  'Kwota transakcji (waluta rachunku)',
                                  'Kwota blokady/zwolnienie blokady',
                                  'Saldo po transakcji'],
                         inplace=True)


    def to_next(self):
        self.current_index += 1
        if self.current_index >= 0 and self.current_index < len(self.df):
            return True
        else:
            return False


    def assign_current(self, category):
        if self.current_index >= 0 and self.current_index < len(self.df):
            current = self.df.iloc[self.current_index].copy()
            current['category'] = category
            self.processed.append(current)
        else:
            raise ValueError('Assigning out of bounds')


    def current(self):
        if self.current_index != -1:
            return self.df.iloc[self.current_index]
        elif self.current_index >= len(self.df):
            return np.empty

    
    def get_processed(self):
        return pd.DataFrame(self.processed)


    def get_last_processed(self):
        if self.processed:
            return self.processed[-1]
        else:
            return None


    def length(self):
        return len(self.df.index)

    def save_processed(self):
        if self.processed:
            out_file_path = 'out/' + self.file[0:-4] +  '_processed.csv'
            pd.DataFrame(self.processed).to_csv(path_or_buf=out_file_path,
                                                sep=';',
                                                index=False)
            # todo: check if saved properly
