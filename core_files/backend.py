from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import numpy as np
import os
import sys
pd.set_option('expand_frame_repr', False)  # To view all the variables in the console


class Covid:

    def __init__(self, by: str, ascending: bool = False) -> None:
        """Scrape and get a dataframe at the end."""

        self.by = by
        self.ascending: bool = ascending

        url = "https://coronavirus.jhu.edu/data/mortality"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html5lib")

        mytable = soup.select("td")
        updated_for = soup.select("strong")

        table_lst = [item.text for item in mytable]

        update_datetime = [item.text for item in updated_for][0]
        regex = r'^This page was '
        update_datetime = re.sub(regex, "", update_datetime)
        self.update_datetime = update_datetime[0].upper() + update_datetime[1:]

        d = {'country': table_lst[0::5], 'confirmed': table_lst[1::5],
             'deaths': table_lst[2::5], 'case_fatality_pct': table_lst[3::5], 'deaths_per_100k_pop': table_lst[4::5]}

        self._df = pd.DataFrame(d)

        # fix types
        self._df['confirmed'] = self._df['confirmed'].apply(lambda x: re.sub(r',', "", x))
        self._df['confirmed'] = pd.to_numeric(self._df['confirmed'])

        self._df['deaths'] = self._df['deaths'].apply(lambda x: re.sub(r',', "", x))
        self._df['deaths'] = pd.to_numeric(self._df['deaths'])

        self._df['case_fatality_pct'] = self._df['case_fatality_pct'].apply(lambda x: re.sub(r'%', "", x))
        self._df['case_fatality_pct'] = pd.to_numeric(self._df['case_fatality_pct'])

        # replace missing values
        self._df['deaths_per_100k_pop'] = self._df['deaths_per_100k_pop'].replace(to_replace='nan', value=np.nan)
        self._df['deaths_per_100k_pop'] = pd.to_numeric(self._df['deaths_per_100k_pop'])

    def top_10_table(self) -> pd.DataFrame:
        """Builds the final dataframe to output. Sorted by 'by'."""

        temp_df = (self._df.sort_values(by=self.by, ascending=self.ascending)
                   .reset_index()
                   .drop('index', axis=1)
                   .reset_index()
                   .rename(columns={"index": "rank"})
                   )
        df_israel = temp_df[temp_df['country'] == 'Israel']
        print('\n', self.update_datetime)
        result_df = pd.concat([temp_df.head(10), df_israel], axis=0)
        hide_index = [''] * len(result_df)
        result_df.index = hide_index
        return result_df

    def write_to_csv(self, path: str) -> None:
        dir_path = '/'.join(path.split('/')[:-1]) + '/'     # get only the directories part
        if not os.path.isdir(dir_path):
            print("The path that was specified does not exist")
            sys.exit()
        else:
            self.top_10_table().to_csv(path, index=False)